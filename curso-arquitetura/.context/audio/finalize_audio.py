from pathlib import Path
import subprocess,json
base=Path.cwd(); metadata=base/'studio/briefings.json';records=json.loads(metadata.read_text())
for r in records:
 n=r['lessonNumber'];dst=base/r['audioPath']; raw=base/f'.context/audio/{n:02d}-elevenlabs.mp3'
 if n==2: source=dst
 elif not raw.exists(): continue
 else: source=raw
 duration=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(source)]))
 if n!=2:
  if duration>240 or duration<180:
   target=235 if duration>240 else 185;tempo=duration/target
   subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(raw),'-af',f'atempo={tempo:.6f}','-codec:a','libmp3lame','-b:a','160k',str(dst)],check=True)
   r['tempoAdjustment']=round(tempo,5)
  else:
   import shutil
   shutil.copy2(raw,dst)
  r['generationSource']='ElevenLabs · Rodrigo Souzax — Educational Friendly · Eleven Multilingual v2 · conta contato@fernandakipper.com verificada'
 r['originalDurationSeconds']=round(duration,3)
 r['durationSeconds']=round(float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(dst)])),3)
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-i',str(dst),'-f','null','-'],check=True)
 r['audioStatus']='generated';r['verification']='Duração medida com ffprobe; decodificação integral com FFmpeg; texto confrontado com roteiro/fontes. Sem escuta humana integral.'
 print(n,r['durationSeconds'],r.get('tempoAdjustment',1),flush=True)
metadata.write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
