import{f as e,p as f}from"./immer-697392e4.js";import{r as n}from"./index-4483060c.js";function c(r){var t=n.useState(function(){return e(typeof r=="function"?r():r,!0)}),u=t[1];return[t[0],n.useCallback(function(o){u(typeof o=="function"?f(o):e(o))},[])]}export{c as i};