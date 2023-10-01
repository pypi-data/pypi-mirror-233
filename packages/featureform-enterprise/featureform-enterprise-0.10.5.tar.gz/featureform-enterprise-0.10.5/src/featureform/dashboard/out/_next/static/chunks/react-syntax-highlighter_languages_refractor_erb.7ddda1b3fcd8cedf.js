"use strict";(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[2584,3047,369],{84790:function(a,b,c){var d=c(56939),e=c(93205);function f(a){var b;a.register(d),a.register(e),(b=a).languages.erb={delimiter:{pattern:/^(\s*)<%=?|%>(?=\s*$)/,lookbehind:!0,alias:"punctuation"},ruby:{pattern:/\s*\S[\s\S]*/,alias:"language-ruby",inside:b.languages.ruby}},b.hooks.add("before-tokenize",function(a){b.languages["markup-templating"].buildPlaceholders(a,"erb",/<%=?(?:[^\r\n]|[\r\n](?!=begin)|[\r\n]=begin\s(?:[^\r\n]|[\r\n](?!=end))*[\r\n]=end)+?%>/g)}),b.hooks.add("after-tokenize",function(a){b.languages["markup-templating"].tokenizePlaceholders(a,"erb")})}a.exports=f,f.displayName="erb",f.aliases=[]},93205:function(a){function b(a){!function(a){function b(a,b){return"___"+a.toUpperCase()+b+"___"}Object.defineProperties(a.languages["markup-templating"]={},{buildPlaceholders:{value:function(c,d,e,f){if(c.language===d){var g=c.tokenStack=[];c.code=c.code.replace(e,function(a){if("function"==typeof f&&!f(a))return a;for(var e,h=g.length;-1!==c.code.indexOf(e=b(d,h));)++h;return g[h]=a,e}),c.grammar=a.languages.markup}}},tokenizePlaceholders:{value:function(c,d){if(c.language===d&&c.tokenStack){c.grammar=a.languages[d];var e=0,f=Object.keys(c.tokenStack);g(c.tokens)}function g(h){for(var i=0;i<h.length&&!(e>=f.length);i++){var j=h[i];if("string"==typeof j||j.content&&"string"==typeof j.content){var k=f[e],l=c.tokenStack[k],m="string"==typeof j?j:j.content,n=b(d,k),o=m.indexOf(n);if(o> -1){++e;var p=m.substring(0,o),q=new a.Token(d,a.tokenize(l,c.grammar),"language-"+d,l),r=m.substring(o+n.length),s=[];p&&s.push.apply(s,g([p])),s.push(q),r&&s.push.apply(s,g([r])),"string"==typeof j?h.splice.apply(h,[i,1].concat(s)):j.content=s}}else j.content&&g(j.content)}return h}}}})}(a)}a.exports=b,b.displayName="markupTemplating",b.aliases=[]},56939:function(a){function b(a){var b,c,d,e;(b=a).languages.ruby=b.languages.extend("clike",{comment:{pattern:/#.*|^=begin\s[\s\S]*?^=end/m,greedy:!0},"class-name":{pattern:/(\b(?:class|module)\s+|\bcatch\s+\()[\w.\\]+|\b[A-Z_]\w*(?=\s*\.\s*new\b)/,lookbehind:!0,inside:{punctuation:/[.\\]/}},keyword:/\b(?:BEGIN|END|alias|and|begin|break|case|class|def|define_method|defined|do|each|else|elsif|end|ensure|extend|for|if|in|include|module|new|next|nil|not|or|prepend|private|protected|public|raise|redo|require|rescue|retry|return|self|super|then|throw|undef|unless|until|when|while|yield)\b/,operator:/\.{2,3}|&\.|===|<?=>|[!=]?~|(?:&&|\|\||<<|>>|\*\*|[+\-*/%<>!^&|=])=?|[?:]/,punctuation:/[(){}[\].,;]/}),b.languages.insertBefore("ruby","operator",{"double-colon":{pattern:/::/,alias:"punctuation"}}),c={pattern:/((?:^|[^\\])(?:\\{2})*)#\{(?:[^{}]|\{[^{}]*\})*\}/,lookbehind:!0,inside:{content:{pattern:/^(#\{)[\s\S]+(?=\}$)/,lookbehind:!0,inside:b.languages.ruby},delimiter:{pattern:/^#\{|\}$/,alias:"punctuation"}}},delete b.languages.ruby.function,d="(?:"+[/([^a-zA-Z0-9\s{(\[<=])(?:(?!\1)[^\\]|\\[\s\S])*\1/.source,/\((?:[^()\\]|\\[\s\S]|\((?:[^()\\]|\\[\s\S])*\))*\)/.source,/\{(?:[^{}\\]|\\[\s\S]|\{(?:[^{}\\]|\\[\s\S])*\})*\}/.source,/\[(?:[^\[\]\\]|\\[\s\S]|\[(?:[^\[\]\\]|\\[\s\S])*\])*\]/.source,/<(?:[^<>\\]|\\[\s\S]|<(?:[^<>\\]|\\[\s\S])*>)*>/.source].join("|")+")",e=/(?:"(?:\\.|[^"\\\r\n])*"|(?:\b[a-zA-Z_]\w*|[^\s\0-\x7F]+)[?!]?|\$.)/.source,b.languages.insertBefore("ruby","keyword",{"regex-literal":[{pattern:RegExp(/%r/.source+d+/[egimnosux]{0,6}/.source),greedy:!0,inside:{interpolation:c,regex:/[\s\S]+/}},{pattern:/(^|[^/])\/(?!\/)(?:\[[^\r\n\]]+\]|\\.|[^[/\\\r\n])+\/[egimnosux]{0,6}(?=\s*(?:$|[\r\n,.;})#]))/,lookbehind:!0,greedy:!0,inside:{interpolation:c,regex:/[\s\S]+/}}],variable:/[@$]+[a-zA-Z_]\w*(?:[?!]|\b)/,symbol:[{pattern:RegExp(/(^|[^:]):/.source+e),lookbehind:!0,greedy:!0},{pattern:RegExp(/([\r\n{(,][ \t]*)/.source+e+/(?=:(?!:))/.source),lookbehind:!0,greedy:!0}],"method-definition":{pattern:/(\bdef\s+)\w+(?:\s*\.\s*\w+)?/,lookbehind:!0,inside:{function:/\b\w+$/,keyword:/^self\b/,"class-name":/^\w+/,punctuation:/\./}}}),b.languages.insertBefore("ruby","string",{"string-literal":[{pattern:RegExp(/%[qQiIwWs]?/.source+d),greedy:!0,inside:{interpolation:c,string:/[\s\S]+/}},{pattern:/("|')(?:#\{[^}]+\}|#(?!\{)|\\(?:\r\n|[\s\S])|(?!\1)[^\\#\r\n])*\1/,greedy:!0,inside:{interpolation:c,string:/[\s\S]+/}},{pattern:/<<[-~]?([a-z_]\w*)[\r\n](?:.*[\r\n])*?[\t ]*\1/i,alias:"heredoc-string",greedy:!0,inside:{delimiter:{pattern:/^<<[-~]?[a-z_]\w*|\b[a-z_]\w*$/i,inside:{symbol:/\b\w+/,punctuation:/^<<[-~]?/}},interpolation:c,string:/[\s\S]+/}},{pattern:/<<[-~]?'([a-z_]\w*)'[\r\n](?:.*[\r\n])*?[\t ]*\1/i,alias:"heredoc-string",greedy:!0,inside:{delimiter:{pattern:/^<<[-~]?'[a-z_]\w*'|\b[a-z_]\w*$/i,inside:{symbol:/\b\w+/,punctuation:/^<<[-~]?'|'$/}},string:/[\s\S]+/}}],"command-literal":[{pattern:RegExp(/%x/.source+d),greedy:!0,inside:{interpolation:c,command:{pattern:/[\s\S]+/,alias:"string"}}},{pattern:/`(?:#\{[^}]+\}|#(?!\{)|\\(?:\r\n|[\s\S])|[^\\`#\r\n])*`/,greedy:!0,inside:{interpolation:c,command:{pattern:/[\s\S]+/,alias:"string"}}}]}),delete b.languages.ruby.string,b.languages.insertBefore("ruby","number",{builtin:/\b(?:Array|Bignum|Binding|Class|Continuation|Dir|Exception|FalseClass|File|Fixnum|Float|Hash|IO|Integer|MatchData|Method|Module|NilClass|Numeric|Object|Proc|Range|Regexp|Stat|String|Struct|Symbol|TMS|Thread|ThreadGroup|Time|TrueClass)\b/,constant:/\b[A-Z][A-Z0-9_]*(?:[?!]|\b)/}),b.languages.rb=b.languages.ruby}a.exports=b,b.displayName="ruby",b.aliases=["rb"]}}])
//# sourceMappingURL=react-syntax-highlighter_languages_refractor_erb.7ddda1b3fcd8cedf.js.map