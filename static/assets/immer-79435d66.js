import{r as g,v as j,R as x}from"./index-17e5916c.js";import{p as I}from"./immer-bb0c084b.js";const y=e=>{let t;const n=new Set,o=(s,d)=>{const c=typeof s=="function"?s(t):s;if(!Object.is(c,t)){const i=t;t=d??(typeof c!="object"||c===null)?c:Object.assign({},t,c),n.forEach(f=>f(t,i))}},r=()=>t,E={setState:o,getState:r,getInitialState:()=>v,subscribe:s=>(n.add(s),()=>n.delete(s)),destroy:()=>{n.clear()}},v=t=e(o,r,E);return E},V=e=>e?y(e):y;var h={exports:{}},R={},w={exports:{}},O={};/**
 * @license React
 * use-sync-external-store-shim.production.js
 *
 * Copyright (c) Meta Platforms, Inc. and affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */var S=g;function $(e,t){return e===t&&(e!==0||1/e===1/t)||e!==e&&t!==t}var A=typeof Object.is=="function"?Object.is:$,F=S.useState,P=S.useEffect,W=S.useLayoutEffect,z=S.useDebugValue;function M(e,t){var n=t(),o=F({inst:{value:n,getSnapshot:t}}),r=o[0].inst,u=o[1];return W(function(){r.value=n,r.getSnapshot=t,m(r)&&u({inst:r})},[e,n,t]),P(function(){return m(r)&&u({inst:r}),e(function(){m(r)&&u({inst:r})})},[e]),z(n),n}function m(e){var t=e.getSnapshot;e=e.value;try{var n=t();return!A(e,n)}catch{return!0}}function _(e,t){return t()}var C=typeof window>"u"||typeof window.document>"u"||typeof window.document.createElement>"u"?_:M;O.useSyncExternalStore=S.useSyncExternalStore!==void 0?S.useSyncExternalStore:C;w.exports=O;var L=w.exports;/**
 * @license React
 * use-sync-external-store-shim/with-selector.production.js
 *
 * Copyright (c) Meta Platforms, Inc. and affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */var p=g,T=L;function U(e,t){return e===t&&(e!==0||1/e===1/t)||e!==e&&t!==t}var B=typeof Object.is=="function"?Object.is:U,q=T.useSyncExternalStore,G=p.useRef,k=p.useEffect,H=p.useMemo,J=p.useDebugValue;R.useSyncExternalStoreWithSelector=function(e,t,n,o,r){var u=G(null);if(u.current===null){var a={hasValue:!1,value:null};u.current=a}else a=u.current;u=H(function(){function E(i){if(!v){if(v=!0,s=i,i=o(i),r!==void 0&&a.hasValue){var f=a.value;if(r(f,i))return d=f}return d=i}if(f=d,B(s,i))return f;var b=o(i);return r!==void 0&&r(f,b)?(s=i,f):(s=i,d=b)}var v=!1,s,d,c=n===void 0?null:n;return[function(){return E(t())},c===null?void 0:function(){return E(c())}]},[t,n,o,r]);var l=q(e,u[0],u[1]);return k(function(){a.hasValue=!0,a.value=l},[l]),J(l),l};h.exports=R;var K=h.exports;const N=j(K),{useDebugValue:Q}=x,{useSyncExternalStoreWithSelector:X}=N;const Y=e=>e;function Z(e,t=Y,n){const o=X(e.subscribe,e.getState,e.getServerState||e.getInitialState,t,n);return Q(o),o}const D=e=>{const t=typeof e=="function"?V(e):e,n=(o,r)=>Z(t,o,r);return Object.assign(n,t),n},re=e=>e?D(e):D,ee=e=>(t,n,o)=>(o.setState=(r,u,...a)=>{const l=typeof r=="function"?I(r):r;return t(l,u,...a)},e(o.setState,n,o)),oe=ee;export{re as c,oe as i};
