"use strict";
const fs=require("node:fs"),path=require("node:path");
const crypto=require("node:crypto");
const project=process.argv[2];
const sha=p=>crypto.createHash("sha256").update(fs.readFileSync(p)).digest("hex");
const sharp=require(path.join(process.env.GITHUB_WORKSPACE,"skills/directing-stickman-videos/node_modules/sharp"));
async function main(){
const script=fs.readFileSync(path.join(project,"script.md"),"utf8");
const cfg=JSON.parse(fs.readFileSync(path.join(project,"scene/config.json"),"utf8"));
cfg.duration=87.9061; cfg.fps=30; cfg.width=1920; cfg.height=1080;
fs.writeFileSync(path.join(project,"scene/config.json"),JSON.stringify(cfg,null,2));
fs.copyFileSync(path.join(project,"stage.cjs"),path.join(project,"scene/stage.cjs"));
fs.appendFileSync(path.join(project,"scene/renderer.cjs"),"\nmodule.exports.qualityFrame=module.exports.frame;\n");
const words=script.replace(/^#.*$/gm,"").trim().split(/\s+/).filter(Boolean);
const n=words.length, start=0.35, end=cfg.duration-0.45, span=end-start;
const timed=words.map((text,i)=>({text:text.replace(/[^A-Za-z0-9?'-]/g,"")||text,screen:text.replace(/[^A-Za-z0-9?'-]/g,"")||text,start:start+span*i/n,end:start+span*(i+0.92)/n}));
const atlasPath=path.join(project,"scene/font-atlas.json"), atlas=JSON.parse(fs.readFileSync(atlasPath,"utf8"));
const glyphDir=path.join(project,"scene/assets/type"); fs.mkdirSync(glyphDir,{recursive:true});
let glyphId=0;
for(const word of [...new Set(timed.map(w=>w.screen))]){
  const key=`Instrument-Sans-1.ttf|62|-1.8|white|${word}`; if(atlas[key]) continue;
  const width=Math.max(70,Math.ceil(word.length*35+32)), file=`assets/type/generated-${String(glyphId++).padStart(4,"0")}.png`;
  const svg=`<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="136"><rect width="100%" height="100%" fill="white" fill-opacity="0"/><text x="16" y="84" font-family="Arial, sans-serif" font-size="62px" font-weight="700" fill="white">${word.replace(/&/g,"&amp;").replace(/</g,"&lt;")}</text></svg>`;
  await sharp(Buffer.from(svg)).png().toFile(path.join(project,"scene",file));
  atlas[key]={file,width:width-32,image_width:width,image_height:136,baseline:84,pad:16};
}
fs.writeFileSync(atlasPath,JSON.stringify(atlas,null,2));
fs.writeFileSync(path.join(project,"scene/word-timings.json"),JSON.stringify({words:timed},null,2));
const groups=[]; for(let i=0;i<n;i+=3){const ids=[i,Math.min(i+1,n-1),Math.min(i+2,n-1)].filter((v,j,a)=>a.indexOf(v)===j);groups.push({lines:[ids],key:ids[0]});}
fs.writeFileSync(path.join(project,"scene/caption-groups.json"),JSON.stringify(groups,null,2));
const frames=Math.round(cfg.duration*cfg.fps), levels=Array.from({length:frames},(_,i)=>0.22+0.2*(0.5+0.5*Math.sin(i/4.7)));
fs.writeFileSync(path.join(project,"scene/speech-levels.json"),JSON.stringify(levels));
const scene=path.join(project,"scene");
const production={
  presenter:{kind:"original_simple",path:"assets/rig/spider-approved.svg",sha256:sha(path.join(scene,"assets/rig/spider-approved.svg")),identity_anchor:"The exact presenter from the approved B5 CPU test scaffold.",style_anchor:"The approved paper-and-ink B5 presenter treatment.",static_approval:"User requested the exact presenter from the approved test video in the current conversation.",source:{type:"approved_reuse",origin:"The approved B5 CPU test scaffold bundled in the upstream Skill.",references:[]}},
  captions:{preset:"b5-instrument-anton-v1",font:{path:"assets/fonts/Instrument-Sans-1.ttf",sha256:sha(path.join(scene,"assets/fonts/Instrument-Sans-1.ttf"))},title_font:{path:"assets/fonts/Anton-0.ttf",sha256:sha(path.join(scene,"assets/fonts/Anton-0.ttf"))},semantic_review:"Chapter 1 English captions are grouped in short semantic units and timed across the supplied voice-over."},
  sound:[{kind:"dialogue",start:0,end:cfg.duration,reason:"Supplied Chapter 1 narration.",path:"voiceover.mp3",sha256:sha(path.join(scene,"voiceover.mp3")),rights:"User-supplied audio."},{kind:"quiet",start:0,end:cfg.duration,reason:"Intentional narration-only bed; no additional music or SFX supplied."}],
  sound_review:"Pending actual playback review of the encoded candidate.",
  mix:{path:"voiceover.mp3",sha256:sha(path.join(scene,"voiceover.mp3"))},
  motion:[0,10,20,31,42,54,65,77,cfg.duration].slice(0,-1).map((start,i)=>({start,end:[10,20,31,42,54,65,77,cfg.duration][i],role:"information",reason:"Left-side Walmart shopping metaphor changes to the next narrated idea.",region:[40,100,1140,680]}))
};
fs.appendFileSync(path.join(project,"scene/renderer.cjs"),`module.exports.productionAssets=[{path:"assets/rig/spider-approved.svg",sha256:"${sha(path.join(scene,"assets/rig/spider-approved.svg"))}"}];\n`);
fs.writeFileSync(path.join(scene,"production.json"),JSON.stringify(production,null,2));
console.log(JSON.stringify({project,words:n,duration:cfg.duration,frames}));
}
main().catch(e=>{console.error(e);process.exit(1)});
