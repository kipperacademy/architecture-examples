from pathlib import Path
import subprocess,json
base=Path.cwd(); records=json.loads((base/'studio/briefings.json').read_text())
for r in records:
 n=r['lessonNumber']
 if n!=2:
  src=base/r['scriptPath']; raw=base/f'.context/audio/{n:02d}.aiff'; dst=base/r['audioPath']
  subprocess.run(['say','-v','Luciana','-r','145','-f',str(src),'-o',str(raw)],check=True)
  duration=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(raw)]))
  target=max(185,min(235,duration)); tempo=duration/target
  subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(raw),'-af',f'atempo={tempo:.6f}','-codec:a','libmp3lame','-q:a','3',str(dst)],check=True)
  r['audioStatus']='generated';r['tempoAdjustment']=round(tempo,4)
 r['durationSeconds']=round(float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(base/r['audioPath'])])),3)
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-i',str(base/r['audioPath']),'-f','null','-'],check=True)
 print(n,r['durationSeconds'],flush=True)
 (base/'studio/briefings.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
