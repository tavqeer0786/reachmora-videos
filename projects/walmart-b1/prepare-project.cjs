"use strict";
const fs=require("node:fs"),path=require("node:path"),cp=require("node:child_process");
const [dir,audio,script,chapter,engine]=process.argv.slice(2);
if(!dir||!audio||!script||!engine)throw new Error("usage: prepare-project.cjs PROJECT AUDIO SCRIPT CHAPTER ENGINE_DIR");
const sharp=require(path.join(engine,"node_modules","sharp"));
const ink="#191916",red="#EC4338",yellow="#F2C84B",paper="#FDFDFC",blue="#DCECF0";
const probe=JSON.parse(cp.execFileSync("ffprobe",["-v","error","-show_format","-of","json",audio],{encoding:"utf8"}));
const duration=Number(probe.format.duration),W=1280,H=720,FPS=30;
const raw=fs.readFileSync(script,"utf8").replace(/^#.*$/gm,"").replace(/\*\*/g,"").trim();
const words=raw.split(/\s+/).filter(Boolean).map(x=>x.replace(/[^A-Za-z0-9?'’-]/g,"")),clean=words.filter(Boolean),captions=[];
const group=5,usable=duration-.35;
for(let i=0;i<clean.length;i+=group){const arr=clean.slice(i,i+group),start=.18+usable*i/clean.length,end=Math.min(duration,start+usable*arr.length/clean.length*.98);captions.push({start:Number(start.toFixed(3)),end:Number(Math.max(start+.18,end).toFixed(3)),text:arr.join(" ")});}
const esc=s=>String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
const svg=(w,h,b)=>`<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}"><rect width="100%" height="100%" fill="${paper}"/>${b}</svg>`;
const L=(d,c=ink,w=7)=>`<path d="${d}" fill="none" stroke="${c}" stroke-width="${w}" stroke-linecap="round" stroke-linejoin="round"/>`;
const T=(s,x,y,size=42,c=ink)=>`<text x="${x}" y="${y}" font-family="Arial, sans-serif" font-weight="700" font-size="${size}" fill="${c}">${esc(s)}</text>`;
function art(kind){
 if(kind==="shopper")return svg(420,560,`<circle cx="210" cy="90" r="58" fill="${paper}" stroke="${ink}" stroke-width="8"/>${L("M185 82q12-12 24 0M232 82q12-12 24 0M188 120q22 18 45 0",ink,7)}${L("M210 148v190M210 190L105 270M210 190L315 245M210 338L145 500M210 338L275 500",ink,9)}<path d="M65 255h45l40 110h170l22-80H120" fill="none" stroke="${ink}" stroke-width="8" stroke-linejoin="round"/><circle cx="150" cy="390" r="13" fill="${paper}" stroke="${ink}" stroke-width="7"/><circle cx="285" cy="390" r="13" fill="${paper}" stroke="${ink}" stroke-width="7"/><path d="M150 330h130" stroke="${red}" stroke-width="8"/>`);
 if(kind==="phone-shopper")return svg(420,560,`<circle cx="210" cy="90" r="58" fill="${paper}" stroke="${ink}" stroke-width="8"/>${L("M185 82q12-12 24 0M232 82q12-12 24 0M190 120q20 16 40 0",ink,7)}${L("M210 148v190M210 205L120 235M210 205L290 100M210 338L145 500M210 338L275 500",ink,9)}<rect x="275" y="55" width="64" height="112" rx="8" fill="${blue}" stroke="${ink}" stroke-width="8"/>${T("APP",286,112,18,red)}${L("M288 128h38M288 140h25",ink,4)}`);
 if(kind==="family")return svg(520,430,`<circle cx="120" cy="90" r="44" fill="${paper}" stroke="${ink}" stroke-width="7"/><circle cx="260" cy="75" r="52" fill="${paper}" stroke="${ink}" stroke-width="7"/><circle cx="390" cy="105" r="38" fill="${paper}" stroke="${ink}" stroke-width="7"/>${L("M120 135v155M120 175L45 235M120 175L185 230M120 290L80 390M120 290L165 390",ink,8)}${L("M260 130v160M260 170L195 220M260 170L330 225M260 290L215 390M260 290L305 390",ink,8)}${L("M390 145v130M390 180L345 225M390 180L435 225M390 275L360 375M390 275L425 375",ink,7)}<rect x="210" y="210" width="120" height="80" fill="#FFF5C7" stroke="${red}" stroke-width="6"/>${L("M230 235h75M230 255h60M230 275h70",red,4)}`);
 if(kind==="tv")return svg(360,260,`<rect x="35" y="25" width="290" height="185" rx="12" fill="${blue}" stroke="${ink}" stroke-width="9"/><rect x="60" y="50" width="240" height="125" fill="${paper}" stroke="${ink}" stroke-width="6"/>${T("SALE",92,120,30,red)}${T("TV",235,140,48,ink)}${L("M120 230h120M180 210v35",ink,8)}`);
 if(kind==="toy")return svg(260,260,`<circle cx="130" cy="130" r="92" fill="#FFF5C7" stroke="${ink}" stroke-width="8"/>${L("M90 125q40-35 80 0M105 155q25 22 50 0",ink,7)}${L("M60 35l-25-25M200 35l25-25M130 25V0",red,7)}`);
 if(kind==="groceries")return svg(330,260,`<path d="M40 45h45l35 125h150l25-90H92" fill="none" stroke="${ink}" stroke-width="9"/><circle cx="125" cy="205" r="16" fill="${paper}" stroke="${ink}" stroke-width="7"/><circle cx="255" cy="205" r="16" fill="${paper}" stroke="${ink}" stroke-width="7"/><path d="M125 125h120M155 85v85M205 85v85" stroke="${red}" stroke-width="7"/><circle cx="165" cy="65" r="22" fill="${yellow}" stroke="${ink}" stroke-width="6"/><path d="M205 44l38 36" stroke="${ink}" stroke-width="8"/>`);
 if(kind==="basket")return svg(330,260,`<path d="M45 75h240l-25 145H70z" fill="#FFF5C7" stroke="${ink}" stroke-width="8"/><path d="M105 75q0-55 60-55t60 55" fill="none" stroke="${ink}" stroke-width="8"/>${L("M95 110v85M145 110v85M195 110v85M245 110v85",red,6)}${T("BUY",115,165,34,red)}`);
 if(kind==="decorations")return svg(300,280,`<path d="M35 220q110-200 230 0" fill="none" stroke="${red}" stroke-width="8"/>${[65,105,150,195,235].map((x,i)=>`<circle cx="${x}" cy="${180-(Math.abs(150-x))*.45}" r="14" fill="${i%2?yellow:red}" stroke="${ink}" stroke-width="5"/>`).join("")}${T("HOLIDAY",65,55,28,ink)}`);
 if(kind==="calendar")return svg(260,280,`<rect x="25" y="35" width="210" height="205" fill="${paper}" stroke="${ink}" stroke-width="8"/><path d="M25 82h210" stroke="${red}" stroke-width="22"/>${[75,115,155,195].map(y=>L(`M45 ${y}h170`,"#aaa",3)).join("")}${[80,125,170].map(x=>L(`M${x} 100v115`,"#aaa",3)).join("")}<circle cx="170" cy="145" r="24" fill="${yellow}" stroke="${red}" stroke-width="5"/>`);
 if(kind==="store")return svg(360,300,`<path d="M35 110l145-70 145 70v150H35z" fill="${paper}" stroke="${ink}" stroke-width="8"/><path d="M20 105h320v48H20z" fill="${red}" stroke="${ink}" stroke-width="8"/>${T("WALMART",85,140,25,"#fff")}${L("M125 175v85M235 175v85M125 175h110M125 260h110",ink,7)}`);
 if(kind==="screen")return svg(340,260,`<rect x="25" y="25" width="290" height="180" rx="10" fill="${blue}" stroke="${ink}" stroke-width="9"/><rect x="50" y="55" width="240" height="120" fill="${paper}" stroke="${ink}" stroke-width="5"/>${T("CHECK STOCK",70,105,24,red)}${L("M70 135h160M70 155h110",ink,5)}${L("M135 215h70M170 205v30",ink,8)}`);
 if(kind==="pickup")return svg(340,300,`<rect x="40" y="85" width="260" height="155" fill="#FFF5C7" stroke="${ink}" stroke-width="8"/>${T("PICKUP",75,150,30,red)}${L("M80 190h170M75 55v35M265 55v35",ink,8)}<circle cx="170" cy="48" r="24" fill="${yellow}" stroke="${ink}" stroke-width="6"/>`);
 if(kind==="delivery")return svg(360,280,`<path d="M35 75h190v145H35zM225 125h65l35 45v50H225z" fill="${paper}" stroke="${ink}" stroke-width="8"/>${T("DELIVERY",60,145,27,red)}<circle cx="105" cy="240" r="18" fill="${paper}" stroke="${ink}" stroke-width="7"/><circle cx="270" cy="240" r="18" fill="${paper}" stroke="${ink}" stroke-width="7"/>${L("M55 55q100-50 200 0",red,7)}`);
 if(kind==="competitors")return svg(400,260,`${T("WALMART",25,70,30,red)}${T("AMAZON",25,130,30,ink)}${T("TARGET",25,190,30,ink)}${L("M180 55h160M180 115h160M180 175h160","#aaa",5)}${L("M180 55l-20-15M180 55l-20 15",red,6)}${L("M340 115l-20-15M340 115l-20 15",ink,6)}${L("M180 175l-20-15M180 175l-20 15",ink,6)}`);
 return svg(300,220,"");
}
async function main(){
 fs.mkdirSync(dir,{recursive:true});const assetDir=path.join(dir,"assets");fs.mkdirSync(assetDir,{recursive:true});
 const kinds=["shopper","phone-shopper","family","tv","toy","groceries","basket","decorations","calendar","store","screen","pickup","delivery","competitors"];
 for(const k of kinds)await sharp(Buffer.from(art(k))).png().toFile(path.join(assetDir,`${k}.png`));
 const bed=path.join(dir,"room-tone.wav");cp.execFileSync("ffmpeg",["-y","-f","lavfi","-i",`anoisesrc=color=pink:amplitude=0.003:duration=${duration.toFixed(3)}:sample_rate=48000`,"-c:a","pcm_s16le",bed],{stdio:"ignore"});
 function text(s,x=86,y=70,size=52,color=ink,w=1080){return {type:"text",text:s,x,y,size,color,w,bold:true};}
 function img(p,x,y,w,keys=[],id=null,motion=null){const v={type:"image",path:p,x,y,w,keys};if(id){v.id=id;v.motion=motion;}return v;}
 function arrow(x,y,w,color=red){return {type:"arrow",x,y,w,color,lineWidth:5,keys:[{t:0,progress:0},{t:.45,progress:1}]};}
 function line(x,y,points,color=ink,lineWidth=4){return {type:"line",x,y,points,color,lineWidth};}
 const A=k=>`assets/${k}.png`;
 function shot(i,start,end){
  const t=i%10,span=end-start,S=[];
  const titles=chapter==="1"?["ONE SHOPPING DAY","THE LIST KEEPS GROWING","PEOPLE BUY IN STAGES","THE SEASON COMES IN WAVES","A SECOND CHANCE","NOT EVERYONE IS READY","ANOTHER REASON TO LOOK","BLACK FRIDAY ISN'T THE FINISH","MORE THAN ONE MOMENT","THE QUESTION"]:["PRICE IS ONLY ONE PART","A STORE AND A SCREEN","THE HOLIDAY LIST","MANY NEEDS. ONE TRIP.","CHECK STOCK FIRST","PICKUP OR DELIVERY","THE SAME SHOPPING SYSTEM","ONE BASKET, MANY DECISIONS","CONVENIENCE HAS A JOB","THE NEXT VISIT"];
  S.push(text(titles[t],86,58,t===0?56:50,t%3===0?red:ink));
  const hero=img(A(chapter==="2"&&t>=4?"phone-shopper":"shopper"),730,35,430,[{t:0,x:730,y:35,angle:-.015},{t:Math.min(.7,span-.5),x:710,y:25,angle:.012},{t:Math.min(1.4,span-.35),x:730,y:35,angle:-.01},{t:Math.min(2.1,span-.2),x:710,y:25,angle:.01},{t:Math.max(2.2,span-.05),x:730,y:35,angle:-.015}],`chapter-${chapter}-hero-${i}`,{role:"actor",reason:"Story-specific shopper gestures toward the current Walmart decision."});S.push(hero);
  if(chapter==="1"){
   if(t===0)S.push(img(A("calendar"),70,235,180),img(A("tv"),300,260,210),arrow(525,350,220),img(A("shopper"),760,200,230));
   if(t===1)S.push(img(A("tv"),70,245,180),img(A("toy"),320,250,170),img(A("decorations"),555,245,190),img(A("groceries"),820,245,210));
   if(t===2)S.push(img(A("tv"),70,260,180),img(A("toy"),325,265,165),img(A("decorations"),570,255,180),img(A("calendar"),835,240,180),text("NOVEMBER → NEXT WEEK → CHRISTMAS",110,520,30,red,900));
   if(t===3)S.push(img(A("calendar"),70,245,180),line(300,350,[[0,0],[160,0],[320,-80],[500,0]],red,7),img(A("decorations"),850,250,210));
   if(t===4)S.push(img(A("calendar"),80,250,180),arrow(310,365,230),img(A("tv"),650,255,190),text("ANOTHER LOOK",660,510,38,red,500));
   if(t===5)S.push(img(A("shopper"),70,180,230),img(A("tv"),380,260,180),text("NOT READY YET",620,300,42,red,400),line(600,370,[[0,0],[230,0]],ink,5));
   if(t===6)S.push(img(A("calendar"),80,245,180),img(A("toy"),350,250,165),arrow(560,365,220),img(A("shopper"),850,195,220));
   if(t===7)S.push(img(A("calendar"),70,245,180),img(A("decorations"),350,245,180),img(A("groceries"),630,240,200),text("STILL SHOPPING",690,510,38,ink,500));
   if(t===8)S.push(img(A("tv"),70,260,180),img(A("toy"),330,255,165),img(A("groceries"),570,245,200),img(A("decorations"),850,250,190));
   if(t===9)S.push(img(A("competitors"),80,250,290),arrow(430,360,220),text("WHY COME BACK?",700,315,42,red,500),img(A("shopper"),900,180,220));
  }else{
   if(t===0)S.push(text("PRICE",100,285,44,red,220),text("CONVENIENCE",430,285,44,ink,360),arrow(650,375,210),img(A("shopper"),900,190,220));
   if(t===1)S.push(img(A("store"),70,230,240),arrow(340,365,160),img(A("screen"),500,235,240),arrow(770,365,160),img(A("phone-shopper"),930,180,220));
   if(t===2)S.push(img(A("family"),65,250,270),img(A("tv"),390,265,175),img(A("toy"),610,255,160),img(A("groceries"),820,250,190));
   if(t===3)S.push(img(A("family"),60,245,270),img(A("groceries"),390,260,190),img(A("decorations"),650,250,185),text("MANY NEEDS → ONE TRIP",390,510,35,red,620));
   if(t===4)S.push(img(A("phone-shopper"),70,180,220),img(A("screen"),400,245,245),arrow(690,365,220),text("CHECK AVAILABILITY",715,500,34,red,500));
   if(t===5)S.push(img(A("pickup"),70,240,230),arrow(340,365,210),img(A("delivery"),660,240,240),text("PICKUP OR DELIVERY",470,510,34,ink,620));
   if(t===6)S.push(img(A("store"),70,235,220),img(A("screen"),360,245,220),img(A("phone-shopper"),680,175,220),arrow(920,365,170));
   if(t===7)S.push(img(A("tv"),70,260,180),img(A("toy"),300,255,160),img(A("groceries"),510,245,190),img(A("decorations"),760,250,185));
   if(t===8)S.push(img(A("pickup"),70,240,220),img(A("delivery"),360,240,230),img(A("store"),670,235,220),text("LESS FRICTION",410,510,38,red,430));
   if(t===9)S.push(img(A("competitors"),70,245,290),arrow(420,365,220),text("WHAT KEEPS THEM?",690,315,42,red,520),img(A("phone-shopper"),925,180,220));
  }
  return {start,end,layers:S};
 }
 const shots=[],count=Math.ceil(duration/3.2);for(let i=0;i<count;i++){const start=Number((i*duration/count).toFixed(3)),end=i===count-1?duration:Number(((i+1)*duration/count).toFixed(3));shots.push(shot(i,start,end));}
 const project={version:1,style:"B1",width:W,height:H,fps:FPS,voice:{path:"narration.mp3",lead:0,tail:0,contains_sfx:false},ambience:[{path:"room-tone.wav",start:0,end:duration,gain:.03,offset:0,loop:true,fadeIn:1,fadeOut:1}],captions,shots,sfx:shots.map((s,i)=>({time:Number((s.start+.25).toFixed(3)),kind:i%3===0?"paper":"tap",gain:.12})),reference_review:{author_id:"codex",capability:{mode:"sample_target",environment:"GitHub Actions CPU with upstream B1 autopilot renderer",limitations:[]}},metadata:{chapter,source_script:path.basename(script),assets:"story-specific Walmart props and shopper poses generated from the chapter beat list"}};
 fs.writeFileSync(path.join(dir,"project.json"),JSON.stringify(project,null,2));console.log(JSON.stringify({dir,duration,words:clean.length,shots:shots.length,captions:captions.length,assets:kinds.length}));
}
main().catch(e=>{console.error(e);process.exit(1)});
