import{s as h,r as f,k as B,a as C,j as N,_ as p,m as T,T as _}from"./index-8e42b600.js";import{z as g,y as j,c as y,a as E,C as P}from"./Button-5c4975e7.js";const b=["className","component"];function I(n={}){const{themeId:t,defaultTheme:c,defaultClassName:o="MuiBox-root",generateClassName:a}=n,m=g("div",{shouldForwardProp:e=>e!=="theme"&&e!=="sx"&&e!=="as"})(h);return f.forwardRef(function(x,l){const s=B(c),r=j(x),{className:d,component:u="div"}=r,i=C(r,b);return N.jsx(m,p({as:u,ref:l,className:y(d,a?a(o):o),theme:t&&s[t]||s},i))})}const M=E("MuiBox",["root"]),R=M,S=T(),v=I({themeId:_,defaultTheme:S,defaultClassName:R.root,generateClassName:P.generate}),k=v;export{k as B};