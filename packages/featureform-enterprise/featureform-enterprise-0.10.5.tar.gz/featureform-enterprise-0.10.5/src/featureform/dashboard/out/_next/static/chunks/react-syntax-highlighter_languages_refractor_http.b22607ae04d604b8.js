"use strict";(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[6508],{49660:function(a){function b(a){!function(a){function b(a){return RegExp("(^(?:"+a+"):[ 	]*(?![ 	]))[^]+","i")}a.languages.http={"request-line":{pattern:/^(?:CONNECT|DELETE|GET|HEAD|OPTIONS|PATCH|POST|PRI|PUT|SEARCH|TRACE)\s(?:https?:\/\/|\/)\S*\sHTTP\/[\d.]+/m,inside:{method:{pattern:/^[A-Z]+\b/,alias:"property"},"request-target":{pattern:/^(\s)(?:https?:\/\/|\/)\S*(?=\s)/,lookbehind:!0,alias:"url",inside:a.languages.uri},"http-version":{pattern:/^(\s)HTTP\/[\d.]+/,lookbehind:!0,alias:"property"}}},"response-status":{pattern:/^HTTP\/[\d.]+ \d+ .+/m,inside:{"http-version":{pattern:/^HTTP\/[\d.]+/,alias:"property"},"status-code":{pattern:/^(\s)\d+(?=\s)/,lookbehind:!0,alias:"number"},"reason-phrase":{pattern:/^(\s).+/,lookbehind:!0,alias:"string"}}},header:{pattern:/^[\w-]+:.+(?:(?:\r\n?|\n)[ \t].+)*/m,inside:{"header-value":[{pattern:b(/Content-Security-Policy/.source),lookbehind:!0,alias:["csp","languages-csp"],inside:a.languages.csp},{pattern:b(/Public-Key-Pins(?:-Report-Only)?/.source),lookbehind:!0,alias:["hpkp","languages-hpkp"],inside:a.languages.hpkp},{pattern:b(/Strict-Transport-Security/.source),lookbehind:!0,alias:["hsts","languages-hsts"],inside:a.languages.hsts},{pattern:b(/[^:]+/.source),lookbehind:!0}],"header-name":{pattern:/^[^:]+/,alias:"keyword"},punctuation:/^:/}}};var c,d=a.languages,e={"application/javascript":d.javascript,"application/json":d.json||d.javascript,"application/xml":d.xml,"text/xml":d.xml,"text/html":d.html,"text/css":d.css,"text/plain":d.plain},f={"application/json":!0,"application/xml":!0};function g(a){var b=a.replace(/^[a-z]+\//,"");return"(?:"+a+"|\\w+/(?:[\\w.-]+\\+)+"+b+"(?![+\\w.-]))"}for(var h in e)if(e[h]){c=c||{};var i=f[h]?g(h):h;c[h.replace(/\//g,"-")]={pattern:RegExp("("+/content-type:\s*/.source+i+/(?:(?:\r\n?|\n)[\w-].*)*(?:\r(?:\n|(?!\n))|\n)/.source+")"+/[^ \t\w-][\s\S]*/.source,"i"),lookbehind:!0,inside:e[h]}}c&&a.languages.insertBefore("http","header",c)}(a)}a.exports=b,b.displayName="http",b.aliases=[]}}])
//# sourceMappingURL=react-syntax-highlighter_languages_refractor_http.b22607ae04d604b8.js.map