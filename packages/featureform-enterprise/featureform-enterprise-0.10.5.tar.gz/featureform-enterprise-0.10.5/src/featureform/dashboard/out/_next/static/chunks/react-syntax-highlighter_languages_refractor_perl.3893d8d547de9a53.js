"use strict";(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[4157],{74212:function(a){function b(a){var b,c;c=/(?:\((?:[^()\\]|\\[\s\S])*\)|\{(?:[^{}\\]|\\[\s\S])*\}|\[(?:[^[\]\\]|\\[\s\S])*\]|<(?:[^<>\\]|\\[\s\S])*>)/.source,(b=a).languages.perl={comment:[{pattern:/(^\s*)=\w[\s\S]*?=cut.*/m,lookbehind:!0,greedy:!0},{pattern:/(^|[^\\$])#.*/,lookbehind:!0,greedy:!0}],string:[{pattern:RegExp(/\b(?:q|qq|qw|qx)(?![a-zA-Z0-9])\s*/.source+"(?:"+[/([^a-zA-Z0-9\s{(\[<])(?:(?!\1)[^\\]|\\[\s\S])*\1/.source,/([a-zA-Z0-9])(?:(?!\2)[^\\]|\\[\s\S])*\2/.source,c].join("|")+")"),greedy:!0},{pattern:/("|`)(?:(?!\1)[^\\]|\\[\s\S])*\1/,greedy:!0},{pattern:/'(?:[^'\\\r\n]|\\.)*'/,greedy:!0}],regex:[{pattern:RegExp(/\b(?:m|qr)(?![a-zA-Z0-9])\s*/.source+"(?:"+[/([^a-zA-Z0-9\s{(\[<])(?:(?!\1)[^\\]|\\[\s\S])*\1/.source,/([a-zA-Z0-9])(?:(?!\2)[^\\]|\\[\s\S])*\2/.source,c].join("|")+")"+/[msixpodualngc]*/.source),greedy:!0},{pattern:RegExp(/(^|[^-])\b(?:s|tr|y)(?![a-zA-Z0-9])\s*/.source+"(?:"+[/([^a-zA-Z0-9\s{(\[<])(?:(?!\2)[^\\]|\\[\s\S])*\2(?:(?!\2)[^\\]|\\[\s\S])*\2/.source,/([a-zA-Z0-9])(?:(?!\3)[^\\]|\\[\s\S])*\3(?:(?!\3)[^\\]|\\[\s\S])*\3/.source,c+/\s*/.source+c].join("|")+")"+/[msixpodualngcer]*/.source),lookbehind:!0,greedy:!0},{pattern:/\/(?:[^\/\\\r\n]|\\.)*\/[msixpodualngc]*(?=\s*(?:$|[\r\n,.;})&|\-+*~<>!?^]|(?:and|cmp|eq|ge|gt|le|lt|ne|not|or|x|xor)\b))/,greedy:!0}],variable:[/[&*$@%]\{\^[A-Z]+\}/,/[&*$@%]\^[A-Z_]/,/[&*$@%]#?(?=\{)/,/[&*$@%]#?(?:(?:::)*'?(?!\d)[\w$]+(?![\w$]))+(?:::)*/,/[&*$@%]\d+/,/(?!%=)[$@%][!"#$%&'()*+,\-.\/:;<=>?@[\\\]^_`{|}~]/],filehandle:{pattern:/<(?![<=])\S*?>|\b_\b/,alias:"symbol"},"v-string":{pattern:/v\d+(?:\.\d+)*|\d+(?:\.\d+){2,}/,alias:"string"},function:{pattern:/(\bsub[ \t]+)\w+/,lookbehind:!0},keyword:/\b(?:any|break|continue|default|delete|die|do|else|elsif|eval|for|foreach|given|goto|if|last|local|my|next|our|package|print|redo|require|return|say|state|sub|switch|undef|unless|until|use|when|while)\b/,number:/\b(?:0x[\dA-Fa-f](?:_?[\dA-Fa-f])*|0b[01](?:_?[01])*|(?:(?:\d(?:_?\d)*)?\.)?\d(?:_?\d)*(?:[Ee][+-]?\d+)?)\b/,operator:/-[rwxoRWXOezsfdlpSbctugkTBMAC]\b|\+[+=]?|-[-=>]?|\*\*?=?|\/\/?=?|=[=~>]?|~[~=]?|\|\|?=?|&&?=?|<(?:=>?|<=?)?|>>?=?|![~=]?|[%^]=?|\.(?:=|\.\.?)?|[\\?]|\bx(?:=|\b)|\b(?:and|cmp|eq|ge|gt|le|lt|ne|not|or|xor)\b/,punctuation:/[{}[\];(),:]/}}a.exports=b,b.displayName="perl",b.aliases=[]}}])
//# sourceMappingURL=react-syntax-highlighter_languages_refractor_perl.3893d8d547de9a53.js.map