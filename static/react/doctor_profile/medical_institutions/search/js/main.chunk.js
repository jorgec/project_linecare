(window.webpackJsonp=window.webpackJsonp||[]).push([[0],{157:function(e,t,n){e.exports=n(387)},387:function(e,t,n){"use strict";n.r(t);n(158);var a=n(1),o=n.n(a),r=n(78),c=n.n(r),i=n(54),l=n(55),s=n(59),u=n(56),m=n(58),d=n(36),p=n(27),f=n(22),h=n.n(f),v=n(28),g="",y=g+"/location/api/v1/regions",b="".concat(g,"/doctor/api/v1/public/medical_institution/type/list"),S=g+"/doctor/api/v1/private/medical_institution/create",E="".concat(g,"/doctor/api/v1/public/medical_institution/list");function k(){var e=Object(p.a)(["\n  option:first-of-type {\n    color: gray;\n  }\n"]);return k=function(){return e},e}var N=v.a.select(k()),w=function(e){function t(){var e,n;Object(i.a)(this,t);for(var a=arguments.length,o=new Array(a),r=0;r<a;r++)o[r]=arguments[r];return(n=Object(s.a)(this,(e=Object(u.a)(t)).call.apply(e,[this].concat(o)))).state={regions:[]},n}return Object(m.a)(t,e),Object(l.a)(t,[{key:"componentDidMount",value:function(){var e=this;h.a.get(y).then(function(t){var n=t.data.map(function(e){return e});e.setState({regions:n})})}},{key:"render",value:function(){var e=this.state.regions,t=this.props.provinces,n=this.props.cities,a=e.map(function(e){var t=e.name,n=e.id;return o.a.createElement("option",{value:n,key:n},t)}),r=t.map(function(e){var t=e.id,n=e.name;return o.a.createElement("option",{value:t,key:t},n)}),c=n.map(function(e){var t=e.id,n=e.name;return o.a.createElement("option",{value:t,key:t},n)});return o.a.createElement("div",{className:"row"},o.a.createElement("div",{className:"col-lg-4 col-sm-12"},o.a.createElement(N,{onChange:this.props.regionSelectedF,value:this.state.selected,className:"form-control"},o.a.createElement("option",{defaultValue:!0},"Select Region"),a||"No options found")),this.props.regionID?o.a.createElement("div",{className:"col-lg-4 col-sm-12"},o.a.createElement(N,{onChange:this.props.provinceSelectedF,className:"form-control"},o.a.createElement("option",{defaultValue:!0},"Select Province"),r||"null")):o.a.createElement("div",{className:"col-lg-4 col-sm-12"},o.a.createElement(N,{onChange:this.props.provinceSelectedF,className:"form-control"},o.a.createElement("option",{defaultValue:!0},"Select Province"))),this.props.provID?o.a.createElement("div",{className:"col-lg-4 col-sm-12"},o.a.createElement(N,{onChange:this.props.citySelectedF,className:"form-control"},o.a.createElement("option",{defaultValue:!0},"Select City"),c||"null")):o.a.createElement("div",{className:"col-lg-4 col-sm-12"},o.a.createElement(N,{onChange:this.props.citySelectedF,className:"form-control"},o.a.createElement("option",{defaultValue:!0},"Select City"))))}}]),t}(a.Component);function C(){var e=Object(p.a)(["\n  text-align: center;\n"]);return C=function(){return e},e}function j(){var e=Object(p.a)(["\n  display: inline-block;\n  border: 4px solid rgba(0, 0, 0, 0.1);\n  border-left-color: #469a27;\n  border-radius: 50%;\n  width: 30px;\n  height: 30px;\n  animation: donut-spin 1.2s linear infinite;\n  @keyframes donut-spin {\n    0% {\n      transform: rotate(0deg);\n    }\n    100% {\n      transform: rotate(360deg);\n    }\n  }\n"]);return j=function(){return e},e}var x=v.a.div(j()),F=v.a.div(C()),O=function(e){return o.a.createElement(F,null,o.a.createElement(x,null))},R=n(153),M=n(389);function _(){var e=Object(p.a)(["\n  display: none; /* Hidden by default */\n  position: fixed; /* Stay in place */\n  z-index: 1; /* Sit on top */\n  left: 0;\n  top: 0;\n  width: 100%; /* Full width */\n  height: 100%; /* Full height */\n  overflow: auto; /* Enable scroll if needed */\n  background-color: rgb(0, 0, 0); /* Fallback color */\n  background-color: rgba(0, 0, 0, 0.4); /* Black w/ opacity */\n\n  /* Modal Content/Box */\n  .modal-content {\n    background-color: #fefefe;\n    margin: 20px auto; /* 15% from the top and centered */\n    padding: 20px;\n    border: 1px solid #888;\n    width: 90%; /* Could be more or less, depending on screen size */\n    @media (min-width: 992px) {\n      width: 40%; /* Could be more or less, depending on screen size */\n    }\n  }\n\n  /* The Close Button */\n  .close {\n    color: #aaa;\n    float: right;\n    font-size: 28px;\n    font-weight: bold;\n  }\n\n  .close:hover,\n  .close:focus {\n    color: black;\n    text-decoration: none;\n    cursor: pointer;\n  }\n  form {\n    label {\n      display: block;\n      input,\n      select {\n        margin-top: 0.5rem;\n      }\n    }\n  }\n"]);return _=function(){return e},e}function D(){var e=Object(p.a)(["\n  .block {\n    display: block;\n  }\n\n  .none {\n    display: none;\n  }\n"]);return D=function(){return e},e}h.a.defaults.xsrfCookieName="csrftoken",h.a.defaults.xsrfHeaderName="X-CSRFToken";var V=v.a.div(D()),I=v.a.div(_()),z=function(e){function t(){var e,n;Object(i.a)(this,t);for(var a=arguments.length,r=new Array(a),c=0;c<a;c++)r[c]=arguments[c];return(n=Object(s.a)(this,(e=Object(u.a)(t)).call.apply(e,[this].concat(r)))).state={regions:[],types:[],name:null,region:null,zipcode:null,province:null,city:null,address:null,type:null},n.handleFormChange=function(e){n.setState(Object(R.a)({},e.target.name,e.target.value))},n.handleFormSubmit=function(e){e.preventDefault();var t=n.state,a=t.name,r=t.region,c=t.zipcode,i=t.province,l=t.city,s=t.address,u=t.type;h.a.post(S,{method:"post",name:a,region:r,zipcode:c,province:i,city:l,address:s,type:u,headers:{Accept:"application/json","Content-Type":"application/json"}}).then(function(e){if(e){var t=e.id;return o.a.createElement(M.a,{to:"".concat(g,"/doctor/settings/medical_institution/connect?id=").concat(t)})}}).catch(function(e){console.log(e)})},n}return Object(m.a)(t,e),Object(l.a)(t,[{key:"componentDidMount",value:function(){var e=this;h.a.get(y).then(function(t){var n=t.data.map(function(e){return e});e.setState({regions:n})}),h.a.get(b).then(function(t){var n=t.data.map(function(e){return e});e.setState({types:n})})}},{key:"render",value:function(){var e=this.state,t=e.regions,n=e.types,a=this.props,r=a.show,c=a.closeModalRef,i=a.regionSelectedF,l=a.regionID,s=a.provinces,u=a.provID,m=a.cities,d=a.provinceSelectedF,p=a.citySelectedF,f=t.map(function(e){var t=e.name,n=e.id;return o.a.createElement("option",{value:n,key:n},t)}),h=n.map(function(e){var t=e.name,n=e.id;return o.a.createElement("option",{value:n,key:n},t)}),v=s.map(function(e){var t=e.id,n=e.name;return o.a.createElement("option",{value:t,key:t},n)}),g=m.map(function(e){var t=e.id,n=e.name;return o.a.createElement("option",{value:t,key:t},n)});return o.a.createElement(V,null,o.a.createElement(I,{className:r?"block":"none"},o.a.createElement("div",{className:"modal-content"},o.a.createElement("span",{onClick:c,className:"close"},"\xd7"),o.a.createElement("form",{action:"POST",onChange:this.handleFormChange,onSubmit:this.handleFormSubmit},o.a.createElement("h4",{className:"text-center"},"Add Medical Institution"),o.a.createElement("div",{className:"form-group"},o.a.createElement("label",{htmlFor:"name"},"Name",o.a.createElement("input",{className:"form-control",type:"text",name:"name"})),o.a.createElement("label",{htmlFor:"type"},"Type",o.a.createElement("select",{className:"form-control",name:"type"},o.a.createElement("option",{defaultValue:!0},"Select Type"),h||"No options found")),o.a.createElement("label",{htmlFor:"region"},"Region",o.a.createElement("select",{onChange:i,value:this.state.selected,className:"form-control",name:"region"},o.a.createElement("option",{defaultValue:!0},"Select Region"),f||"No options found")),l?o.a.createElement("label",{htmlFor:"province"},"Province",o.a.createElement("select",{className:"form-control",name:"province",onChange:d},o.a.createElement("option",{defaultValue:!0},"Select Province"),v||"null")):o.a.createElement("label",{htmlFor:"province"},"Province",o.a.createElement("select",{className:"form-control",name:"province",onChange:d},o.a.createElement("option",{defaultValue:!0},"Select Province"))),u?o.a.createElement("label",{htmlFor:"city"},"City",o.a.createElement("select",{className:"form-control",name:"city",onChange:p},o.a.createElement("option",{defaultValue:!0},"Select City"),g||"null")):o.a.createElement("label",{htmlFor:"city"},"City",o.a.createElement("select",{className:"form-control",name:"city",onChange:p},o.a.createElement("option",{defaultValue:!0},"Select City"))),o.a.createElement("label",{htmlFor:"address"},"Address",o.a.createElement("input",{className:"form-control",type:"text",name:"address"})),o.a.createElement("label",{htmlFor:"zipcode"},"Zipcode",o.a.createElement("input",{className:"form-control",type:"number",name:"zipcode"}))),o.a.createElement("button",{type:"submit",className:"btn btn-primary btn-block mb-2"},"Submit")))))}}]),t}(a.Component);function q(){var e=Object(p.a)(["\n  display: flex;\n  flex-direction: row;\n  align-items: stretch;\n  ul {\n    width: 100%;\n    &:nth-child(1) {\n      flex: 1;\n      @media (min-width: 1200px) {\n        flex: 1;\n      }\n    }\n    &:nth-child(2) {\n      flex: 1;\n      .list-group-item {\n        text-align: center;\n        position: relative;\n        background-color: #469a27;\n        border: none;\n        margin: 0;\n        color: #fff;\n        /* border-radius: 0; */\n        i {\n          position: absolute;\n          left: 15px;\n          top: 17px;\n        }\n        &:hover {\n          background-color: #397c1f;\n        }\n      }\n    }\n  }\n"]);return q=function(){return e},e}function A(){var e=Object(p.a)(["\n  /* display: flex; */\n  flex-direction: column;\n  justify-content: center;\n  align-items: center;\n  margin-top: 1rem;\n  select {\n    margin-bottom: 1rem;\n    option {\n      &:first-of-type {\n        color: rgba(0, 0, 0, 0.5);\n      }\n    }\n  }\n  input {\n    margin-bottom: 1rem;\n  }\n  p,\n  a {\n    margin-top: 1rem;\n  }\n"]);return A=function(){return e},e}var P=v.a.div(A()),T=v.a.div(q()),B=function(e){function t(){var e,n;Object(i.a)(this,t);for(var a=arguments.length,o=new Array(a),r=0;r<a;r++)o[r]=arguments[r];return(n=Object(s.a)(this,(e=Object(u.a)(t)).call.apply(e,[this].concat(o)))).state={addresses:[],searchResults:[],responseReceived:!1,provinces:[],regSelected:"",cities:[],provSelected:"",loading:!1,endpoint:E,queryString:{location:{name:null,id:0}},showModal:!1},n.handleChange=function(e){var t=Object(d.a)(Object(d.a)(n));if(""===e.target.value)n.setState({searchResults:[],responseReceived:!1});else if(e.target.value.length>=3){var a=E+"?"+n.makeQueryString(e.target.value);n.setState({loading:!0}),h.a.get(a).then(function(e){var n=e.data.map(function(e){return[e.id,e.name]});t.setState({loading:!1}),t.setState({responseReceived:!0}),t.setState({searchResults:n})}).catch(function(e){t.setState({responseReceived:!1}),console.log(e)}).then(function(){})}},n.regionSelected=function(e){n.setState({regSelected:e.target.value},function(){var e=n.state.regSelected,t=Object(d.a)(Object(d.a)(n));n.setState({cities:[]}),n.setState({queryString:{location:{name:"region",id:e}}}),n.setState({provinces:[],endpoint:"".concat(g,"/location/api/v1/provinces_of_region?region=").concat(e)}),h.a.get("".concat(g,"/location/api/v1/provinces_of_region?region=").concat(e)).then(function(e){var n=e.data.map(function(e){return e});t.setState({provinces:n})})})},n.provinceSelected=function(e){n.setState({provSelected:e.target.value},function(){var e=n.state.provSelected,t=Object(d.a)(Object(d.a)(n));n.setState({cities:[]}),n.setState({queryString:{location:{name:"province",id:e}}}),h.a.get("".concat(g,"/location/api/v1/cities_of_province?province=").concat(e)).then(function(e){var n=e.data.map(function(e){return e});t.setState({cities:n})})})},n.citySelected=function(e){n.setState({queryString:{location:{name:"city",id:e.target.value}}})},n.handleShowModal=function(){n.setState({showModal:!0})},n.handleCloseModal=function(){n.setState({showModal:!1})},n}return Object(m.a)(t,e),Object(l.a)(t,[{key:"findMatches",value:function(e,t){return t.filter(function(t){var n=new RegExp(e,"gi");return t.name.match(n)})}},{key:"makeQueryString",value:function(e){var t="s="+e;return this.state.queryString.location.name&&(t=t+"&"+this.state.queryString.location.name+"="+this.state.queryString.location.id),t}},{key:"render",value:function(){var e,t=this.state.searchResults,n=this.state.loading;return e=t.map(function(e){return o.a.createElement(T,{key:e[0]},o.a.createElement("ul",{className:"list-group"},o.a.createElement("li",{className:"list-group-item"},o.a.createElement("a",{href:"".concat(g,"/doctor/settings/medical_institution/connect?id=").concat(e[0])},e[1]))),o.a.createElement("ul",{className:"list-group"},o.a.createElement("a",{href:"".concat(g,"/doctor/settings/medical_institution/connect?id=").concat(e[0]),className:"list-group-item"},o.a.createElement("i",{className:"fas fa-link"}),"Connect to this institution")))}),o.a.createElement(P,{className:"container"},o.a.createElement("input",{className:"form-control",onChange:this.handleChange,type:"text",placeholder:"Search..."}),o.a.createElement(w,{regionSelectedF:this.regionSelected,provinces:this.state.provinces,regionID:this.state.regSelected,provinceSelectedF:this.provinceSelected,cities:this.state.cities,provID:this.state.provSelected,citySelectedF:this.citySelected}),n?o.a.createElement(O,null):this.state.responseReceived?0===t.length?o.a.createElement("p",null,"No results found!"," ",o.a.createElement("button",{onClick:this.handleShowModal},"Add a hospital or clinic?")):e:o.a.createElement("p",null,"\xa0"),o.a.createElement(z,{show:this.state.showModal,closeModalRef:this.handleCloseModal,regionSelectedF:this.regionSelected,provinceSelectedF:this.provinceSelected,regionID:this.state.regSelected,provinces:this.state.provinces,cities:this.state.cities,provID:this.state.provSelected,citySelectedF:this.citySelected}))}}]),t}(a.Component);Boolean("localhost"===window.location.hostname||"[::1]"===window.location.hostname||window.location.hostname.match(/^127(?:\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}$/));c.a.render(o.a.createElement(B,null),document.getElementById("root")),"serviceWorker"in navigator&&navigator.serviceWorker.ready.then(function(e){e.unregister()})}},[[157,2,1]]]);
//# sourceMappingURL=main.aad297cc.chunk.js.map