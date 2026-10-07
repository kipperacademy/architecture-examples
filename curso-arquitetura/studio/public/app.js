'use strict';
let state = { lessons: [] };
let selectedId = localStorage.getItem('studio.selectedLesson');
let busy = false;
let toastTimer;
const $ = (id) => document.getElementById(id);
const esc = (value) => String(value ?? '').replace(/[&<>"']/g, (c) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const statuses = { queue:'Na fila', recording:'Gravando', editing:'Em edição' };
const syncFailed = (lesson) => ['error','failed'].includes(lesson.syncStatus);
const syncPending = (lesson) => ['pending','syncing'].includes(lesson.syncStatus);
function safeUrl(url) { if (!url) return ''; try { const parsed = new URL(url, location.origin); return ['http:','https:'].includes(parsed.protocol) ? esc(url) : ''; } catch { return ''; } }
function lessonRoute() { const path = location.protocol === 'file:' ? location.hash.slice(1) : location.pathname; const match = path.match(/^\/aulas\/([^/]+)\/?$/); if (!match) return null; try { return decodeURIComponent(match[1]); } catch { return '__invalid__'; } }
function navigateToLesson(id) { const path = id ? `/aulas/${encodeURIComponent(id)}` : '/'; history.pushState({}, '', location.protocol === 'file:' ? `#${path}` : path); if(id) {selectedId=id;localStorage.setItem('studio.selectedLesson',id);} render();window.scrollTo({top:0,behavior:'instant'}); }
window.addEventListener('popstate',()=>render());
function number(lesson) { return String(lesson.number ?? state.lessons.indexOf(lesson)+1).padStart(2,'0'); }
function toast(message, error = false) { clearTimeout(toastTimer); $('toast').textContent = message; $('toast').classList.toggle('error', error); $('toast').hidden = false; toastTimer = setTimeout(() => $('toast').hidden = true, error ? 9000 : 4500); }
async function request(path, options = {}) { const response = await fetch(path, {headers: {'Content-Type':'application/json'}, ...options}); let data; try { data = await response.json(); } catch { throw new Error('Não foi possível ler a resposta do estúdio.'); } if (!response.ok) throw new Error(data.error || data.message || 'Não foi possível concluir esta ação.'); return data; }
function accept(data) { const next = data.state || data; if (!Array.isArray(next.lessons)) throw new Error('A lista de aulas está indisponível.'); if (JSON.stringify(state) === JSON.stringify(next)) return; state = next; if (!state.lessons.some(l => String(l.id) === String(selectedId))) selectedId = (state.lessons.find(l => l.status === 'recording') || state.lessons.find(l => l.status === 'queue') || state.lessons[0])?.id; render(); }
async function refresh(silent = false) { try { accept(await request('/api/state')); $('connection').className = 'connection online'; $('connection').innerHTML = '<span class="connection-dot"></span>Estúdio conectado'; } catch (error) { $('connection').className = 'connection error'; $('connection').innerHTML = '<span class="connection-dot"></span>Conexão indisponível'; if (!silent) toast(error.message, true); if (!state.lessons.length) $('board').innerHTML = '<div class="loading">Não foi possível carregar as aulas. Use Atualizar para tentar novamente.</div>'; } }
function render() {
  const editing = state.lessons.filter(l => l.status === 'editing').length;
  const left = state.lessons.length-editing;
  $('progressCount').textContent = `${editing} / ${state.lessons.length}`;
  $('progressFill').style.width = `${state.lessons.length ? editing/state.lessons.length*100 : 0}%`;
  $('remaining').textContent = left ? `${left} ${left === 1 ? 'aula para gravar' : 'aulas para gravar'}` : 'Todas as aulas foram gravadas';
  if (state.sessionDate) { const date = new Date(`${state.sessionDate.slice(0,10)}T12:00:00`); if (!isNaN(date)) $('sessionDate').textContent = date.toLocaleDateString('pt-BR',{weekday:'long',day:'numeric',month:'long'}).toUpperCase(); }
  const columns = [['queue','Fila de gravação','Sua fila está concluída.'],['recording','Gravando','Tudo pronto para começar.'],['editing','Edição','As aulas concluídas chegam aqui.']];
  $('board').innerHTML = columns.map(([status,title,empty]) => { const lessons = state.lessons.filter(l => l.status === status); return `<div class="column" data-status="${status}"><h3 class="column-heading"><span class="dot"></span>${title}<span class="count">${lessons.length}</span></h3><div class="cards">${lessons.length ? lessons.map(l => `<button class="lesson-card ${String(l.id)===String(selectedId)?'selected':''}" data-lesson="${esc(l.id)}" aria-pressed="${String(l.id)===String(selectedId)}"><span class="card-top"><span class="lesson-number">AULA ${esc(number(l))}</span><span class="card-arrow">↗</span></span><span class="card-title">${esc(l.title)}</span><span class="card-bottom">${status==='recording'?'<span class="badge red">● Em gravação</span>':status==='editing'?`<span class="badge ${syncFailed(l)?'red':syncPending(l)?'neutral':''}">${syncFailed(l)?'Pora: tentar novamente':syncPending(l)?'Sincronizando Pora': 'Gravada'}</span>`:`${syncFailed(l)?'<span class="badge red">Pora: tentar novamente</span>':syncPending(l)?'<span class="badge neutral">Sincronizando Pora</span>':''}<span>${l.date ? 'Prazo Pora · '+esc(new Date(l.date.slice(0,10)+'T12:00:00').toLocaleDateString('pt-BR',{day:'2-digit',month:'2-digit'})) : 'A preparar'}</span>`}</span></button>`).join('') : `<div class="empty-column">${empty}</div>`}</div></div>`; }).join('');
  $('board').querySelectorAll('[data-lesson]').forEach(button => button.addEventListener('click',() => {navigateToLesson(button.dataset.lesson);}));
  const completed = Array.isArray(state.completedLessons) ? state.completedLessons : [];
  $('completedLessons').hidden = !completed.length;
  $('completedLessons').innerHTML = completed.map(l => `<span class="completed-intro"><span class="badge">✓ Já gravada · Publicada</span>${safeUrl(l.postLink) ? `<a href="${safeUrl(l.postLink)}" target="_blank" rel="noopener noreferrer">${esc(l.title)} ↗</a>` : esc(l.title)}</span>`).join('');
  const routeId = lessonRoute();
  const detailPage = routeId !== null;
  $('workspace').classList.toggle('detail-page', detailPage);
  document.querySelector('.intro').hidden = detailPage;
  document.querySelector('.session-bar').hidden = detailPage;
  $('completedLessons').hidden = detailPage || !completed.length;
  document.querySelector('.pipeline').hidden = detailPage;
  $('briefing').hidden = !detailPage;
  $('lessonNavigation').hidden = !detailPage;
  if (detailPage) {
    selectedId = routeId;
    const lesson = state.lessons.find(l=>String(l.id)===String(routeId));
    if(lesson) { $('lessonPageLabel').textContent = `AULA ${number(lesson)} · PREPARAÇÃO`; renderBriefing(); }
    else { $('lessonPageLabel').textContent = 'AULA NÃO ENCONTRADA'; $('briefing').innerHTML='<div class="empty-detail"><h2>Aula não encontrada.</h2><p>Volte para a fila e selecione uma das aulas disponíveis.</p></div>'; }
  }
}
function renderBriefing() {
  if (!lessonRoute()) return;
  const lesson = state.lessons.find(l => String(l.id)===String(selectedId));
  if (!lesson) return;
  const priorAudio = $('briefing').querySelector('audio');
  const audioPosition = priorAudio && priorAudio.dataset.lesson === String(lesson.id) ? priorAudio.currentTime : 0;
  const playing = priorAudio && !priorAudio.paused && priorAudio.dataset.lesson === String(lesson.id);
  let checked = []; try { checked = JSON.parse(localStorage.getItem(`studio.checks.${lesson.id}`) || '[]'); } catch {}
  const points = Array.isArray(lesson.points) ? lesson.points : [];
  const boardUrl = safeUrl(lesson.excalidrawUrl);
  const audioUrl = safeUrl(lesson.audioUrl);
  const examples = Array.isArray(lesson.examples) ? lesson.examples : [];
  let action = '';
  if (lesson.status === 'queue') action = `<button class="primary record" id="start" ${busy?'disabled':''}><span>${busy?'Preparando…':'Iniciar gravação'}</span><span>●</span></button><p class="action-note">Abra seu material e confira os pontos antes de começar.</p>`;
  if (lesson.status === 'recording') action = `<button class="primary" id="finish" ${busy?'disabled':''}><span>${busy?'Concluindo…':'Concluir gravação'}</span><span>✓</span></button><p class="action-note">Ao concluir, a aula segue para Edição no Pora.</p>`;
  if (lesson.status === 'editing') action = `${syncFailed(lesson)?'<p class="sync-warning">A gravação foi salva. A mudança para Edição no Pora ainda precisa ser sincronizada.</p><button class="primary" id="retry" '+(busy?'disabled':'')+'><span>Tentar sincronizar novamente</span><span>↻</span></button>':`<div class="completed-label"><span>✓</span>${syncPending(lesson)?'Gravação salva · sincronizando Pora':'Gravação concluída'}</div><p class="action-note">${syncPending(lesson)?'Aguardando a confirmação da mudança no Pora.':lesson.poraStatus?'Pora: '+esc(lesson.poraStatus):'Esta aula está na etapa de edição.'}</p>`}`;
  if (lesson.status === 'queue' && (syncFailed(lesson) || syncPending(lesson))) action += `<p class="${syncFailed(lesson)?'sync-warning':'action-note'}">${syncFailed(lesson)?'A aula voltou para a fila. A mudança no Pora será tentada novamente.':'Aula na fila · sincronizando Gravação pendente no Pora.'}</p>${syncFailed(lesson)?`<button class="secondary" id="retry" ${busy?'disabled':''}>Tentar sincronizar novamente</button>`:''}`;
  if (['recording','editing'].includes(lesson.status)) action += `<button class="secondary" id="requeue" ${busy?'disabled':''}>↶ Voltar para a fila</button>`;
  const pointDetails = Array.isArray(lesson.pointDetails) ? lesson.pointDetails : [];
  function details(index) {const detail = pointDetails[index]; if (!detail) return ''; return `<div class="point-details">${[['definition','O que é'],['mechanism','Como funciona'],['example','Na demo'],['teachingCue','Pergunta para o aluno']].filter(([key])=>detail[key]).map(([key,label])=>`<p><strong>${label}</strong>${esc(detail[key])}</p>`).join('')}</div>`;}
  $('briefing').innerHTML = `<div class="briefing-top"><div class="briefing-overline"><span class="eyebrow" style="margin:0">PREPARAÇÃO · AULA ${esc(number(lesson))}</span><span class="badge ${lesson.status==='recording'?'red':''}">${statuses[lesson.status]||esc(lesson.status)}</span></div><h2>${esc(lesson.title)}</h2><p class="briefing-summary">${esc(lesson.summary||'O resumo desta aula ainda não está disponível.')}</p></div><div class="briefing-body"><section class="detail-section"><h3 class="detail-label">PONTOS QUE NÃO PODEM FALTAR</h3>${points.length?`<ul class="checklist">${points.map((point,index)=>`<li><label><input type="checkbox" data-point="${index}" ${checked.includes(index)?'checked':''}><span>${esc(typeof point === 'string'?point:point.text||point.title)}</span></label>${details(index)}</li>`).join('')}</ul>`:'<p class="missing">Os pontos desta aula ainda estão sendo preparados.</p>'}</section><section class="detail-section"><h3 class="detail-label">OUÇA ANTES DE GRAVAR</h3><div class="audio-box">${audioUrl?`<div class="audio-caption"><span>Preparação da aula</span><label aria-label="Velocidade do áudio"><select id="audioSpeed"><option value="1">1×</option><option value="1.25">1,25×</option><option value="1.5">1,5×</option></select></label></div><audio data-lesson="${esc(lesson.id)}" controls preload="none" src="${audioUrl}">Seu navegador não suporta áudio.</audio>`:'<p class="missing">Áudio de preparação ainda indisponível.</p>'}</div></section><section class="detail-section"><h3 class="detail-label">MATERIAL PARA A AULA</h3><div class="material-links">${boardUrl?`<a class="material-link" href="${boardUrl}" target="_blank" rel="noopener noreferrer"><span class="link-icon">◇</span><span class="link-copy">Abrir Excalidraw<small>Diagrama e sequência visual da aula</small></span><span>↗</span></a>`:'<p class="missing">Link do Excalidraw ainda indisponível.</p>'}${examples.map(example=>`<button class="material-link" data-example="${esc(example.id)}" ${busy?'disabled':''}><span class="link-icon">⌘</span><span class="link-copy">${esc(example.label||'Abrir exemplo de código')}<small>Abrir no Zed · somente arquivos fonte</small></span><span>↗</span></button>`).join('')}${!examples.length?'<p class="missing">Nenhum exemplo de código associado a esta aula.</p>':''}</div></section></div><div class="action-area">${action}</div>`;
  $('briefing').querySelectorAll('[data-point]').forEach(input=>input.addEventListener('change',()=>{ const values = [...$('briefing').querySelectorAll('[data-point]:checked')].map(i=>Number(i.dataset.point)); localStorage.setItem(`studio.checks.${lesson.id}`,JSON.stringify(values)); }));
  const audio = $('briefing').querySelector('audio');
  if (audio) { if (audioPosition) audio.addEventListener('loadedmetadata',()=>{audio.currentTime=audioPosition;if(playing)audio.play().catch(()=>{});},{once:true}); audio.addEventListener('error',()=>toast('Não foi possível carregar o áudio de preparação.',true)); $('audioSpeed').addEventListener('change',()=>audio.playbackRate=Number($('audioSpeed').value)); }
  $('start')?.addEventListener('click',()=>mutate(`/api/lessons/${encodeURIComponent(lesson.id)}/start`,'Gravação iniciada. Boa aula!'));
  $('finish')?.addEventListener('click',()=>mutate(`/api/lessons/${encodeURIComponent(lesson.id)}/finish`,'Gravação concluída.'));
  $('requeue')?.addEventListener('click',()=>mutate(`/api/lessons/${encodeURIComponent(lesson.id)}/requeue`,'Aula devolvida para a fila.'));
  $('retry')?.addEventListener('click',()=>mutate(`/api/lessons/${encodeURIComponent(lesson.id)}/retry-sync`,'Sincronização atualizada.'));
  $('briefing').querySelectorAll('[data-example]').forEach(button=>button.addEventListener('click',async()=>{button.disabled=true;try{await request(`/api/examples/${encodeURIComponent(button.dataset.example)}/open`,{method:'POST'});toast('Exemplo aberto para a aula.');}catch(error){toast(error.message,true);}finally{button.disabled=false;}}));
}
async function mutate(path,message) { if(busy)return;busy=true;renderBriefing();try{const data=await request(path,{method:'POST'});accept(data);const lesson=state.lessons.find(l=>String(l.id)===String(selectedId));if(syncFailed(lesson||{}))toast('Progresso salvo. A sincronização com o Pora precisa ser tentada novamente.',true);else if(syncPending(lesson||{}))toast('Progresso salvo. Sincronizando a etapa no Pora.');else toast(message);}catch(error){toast(error.message,true);await refresh(true);}finally{busy=false;renderBriefing();} }
$('backToQueue').addEventListener('click',(event)=>{event.preventDefault();navigateToLesson(null);});
$('refresh').addEventListener('click',()=>refresh());
refresh();
setInterval(()=>{const audio=$('briefing').querySelector('audio');if(!busy && (!audio || audio.paused))refresh(true);},15000);
