"use strict";(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[7899,3047],{13294:function(a,b,c){var d=c(93205);function e(a){var b,c,e;a.register(d),(b=a).languages.django={comment:/^\{#[\s\S]*?#\}$/,tag:{pattern:/(^\{%[+-]?\s*)\w+/,lookbehind:!0,alias:"keyword"},delimiter:{pattern:/^\{[{%][+-]?|[+-]?[}%]\}$/,alias:"punctuation"},string:{pattern:/("|')(?:\\.|(?!\1)[^\\\r\n])*\1/,greedy:!0},filter:{pattern:/(\|)\w+/,lookbehind:!0,alias:"function"},test:{pattern:/(\bis\s+(?:not\s+)?)(?!not\b)\w+/,lookbehind:!0,alias:"function"},function:/\b[a-z_]\w+(?=\s*\()/i,keyword:/\b(?:and|as|by|else|for|if|import|in|is|loop|not|or|recursive|with|without)\b/,operator:/[-+%=]=?|!=|\*\*?=?|\/\/?=?|<[<=>]?|>[=>]?|[&|^~]/,number:/\b\d+(?:\.\d+)?\b/,boolean:/[Ff]alse|[Nn]one|[Tt]rue/,variable:/\b\w+\b/,punctuation:/[{}[\](),.:;]/},c=/\{\{[\s\S]*?\}\}|\{%[\s\S]*?%\}|\{#[\s\S]*?#\}/g,e=b.languages["markup-templating"],b.hooks.add("before-tokenize",function(a){e.buildPlaceholders(a,"django",c)}),b.hooks.add("after-tokenize",function(a){e.tokenizePlaceholders(a,"django")}),b.languages.jinja2=b.languages.django,b.hooks.add("before-tokenize",function(a){e.buildPlaceholders(a,"jinja2",c)}),b.hooks.add("after-tokenize",function(a){e.tokenizePlaceholders(a,"jinja2")})}a.exports=e,e.displayName="django",e.aliases=["jinja2"]},93205:function(a){function b(a){!function(a){function b(a,b){return"___"+a.toUpperCase()+b+"___"}Object.defineProperties(a.languages["markup-templating"]={},{buildPlaceholders:{value:function(c,d,e,f){if(c.language===d){var g=c.tokenStack=[];c.code=c.code.replace(e,function(a){if("function"==typeof f&&!f(a))return a;for(var e,h=g.length;-1!==c.code.indexOf(e=b(d,h));)++h;return g[h]=a,e}),c.grammar=a.languages.markup}}},tokenizePlaceholders:{value:function(c,d){if(c.language===d&&c.tokenStack){c.grammar=a.languages[d];var e=0,f=Object.keys(c.tokenStack);g(c.tokens)}function g(h){for(var i=0;i<h.length&&!(e>=f.length);i++){var j=h[i];if("string"==typeof j||j.content&&"string"==typeof j.content){var k=f[e],l=c.tokenStack[k],m="string"==typeof j?j:j.content,n=b(d,k),o=m.indexOf(n);if(o> -1){++e;var p=m.substring(0,o),q=new a.Token(d,a.tokenize(l,c.grammar),"language-"+d,l),r=m.substring(o+n.length),s=[];p&&s.push.apply(s,g([p])),s.push(q),r&&s.push.apply(s,g([r])),"string"==typeof j?h.splice.apply(h,[i,1].concat(s)):j.content=s}}else j.content&&g(j.content)}return h}}}})}(a)}a.exports=b,b.displayName="markupTemplating",b.aliases=[]}}])
//# sourceMappingURL=react-syntax-highlighter_languages_refractor_django.94aeee1e71aa34e7.js.map