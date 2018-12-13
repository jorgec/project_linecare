(window.webpackJsonp=window.webpackJsonp||[]).push([[0],{188:function(e,t,n){e.exports=n(416)},416:function(e,t,n){"use strict";n.r(t);n(189);var a=n(0),o=n.n(a),r=n(72),i=n.n(r),l=n(53),c=n(45),s=n(56),d=n(54),m=n(57),u=n(2),p=n(19),h=n(27),f=n.n(h),g=n(20),v=n(421),b="",y=b+"/location/api/v1/regions",E="".concat(b,"/doctor/api/v1/public/medical_institution/type/list"),S=b+"/receptionist/api/v1/private/medical_institution/create",k="".concat(b,"/doctor/api/v1/public/medical_institution/list");function w(){var e=Object(p.a)(["\n  option:first-of-type {\n    color: gray;\n  }\n"]);return w=function(){return e},e}var N=g.a.select(w()),C=function(e){function t(){var e,n;Object(l.a)(this,t);for(var a=arguments.length,o=new Array(a),r=0;r<a;r++)o[r]=arguments[r];return(n=Object(s.a)(this,(e=Object(d.a)(t)).call.apply(e,[this].concat(o)))).state={regions:[]},n}return Object(m.a)(t,e),Object(c.a)(t,[{key:"componentDidMount",value:function(){var e=this;f.a.get(y).then(function(t){var n=t.data.map(function(e){return e});e.setState({regions:n})})}},{key:"render",value:function(){var e=this.state.regions,t=this.props.provinces,n=this.props.cities,a=e.map(function(e){var t=e.name,n=e.id;return o.a.createElement("option",{value:n,key:n},t)}),r=t.map(function(e){var t=e.id,n=e.name;return o.a.createElement("option",{value:t,key:t},n)}),i=n.map(function(e){var t=e.id,n=e.name;return o.a.createElement("option",{value:t,key:t},n)});return o.a.createElement("div",{className:"row"},o.a.createElement("div",{className:"col-lg-4 col-sm-12"},o.a.createElement(N,{onChange:this.props.regionSelectedF,value:this.state.selected,className:"form-control"},o.a.createElement("option",{defaultValue:!0},"Select Region"),a||"No options found")),this.props.regionID?o.a.createElement("div",{className:"col-lg-4 col-sm-12"},o.a.createElement(N,{onChange:this.props.provinceSelectedF,className:"form-control"},o.a.createElement("option",{defaultValue:!0},"Select Province"),r||"null")):o.a.createElement("div",{className:"col-lg-4 col-sm-12"},o.a.createElement(N,{onChange:this.props.provinceSelectedF,className:"form-control"},o.a.createElement("option",{defaultValue:!0},"Select Province"))),this.props.provID?o.a.createElement("div",{className:"col-lg-4 col-sm-12"},o.a.createElement(N,{onChange:this.props.citySelectedF,className:"form-control"},o.a.createElement("option",{defaultValue:!0},"Select City"),i||"null")):o.a.createElement("div",{className:"col-lg-4 col-sm-12"},o.a.createElement(N,{onChange:this.props.citySelectedF,className:"form-control"},o.a.createElement("option",{defaultValue:!0},"Select City"))))}}]),t}(a.Component);function j(){var e=Object(p.a)(["\n  text-align: center;\n"]);return j=function(){return e},e}function x(){var e=Object(p.a)(["\n  display: inline-block;\n  border: 4px solid rgba(0, 0, 0, 0.1);\n  border-left-color: #469a27;\n  border-radius: 50%;\n  width: 30px;\n  height: 30px;\n  animation: donut-spin 1.2s linear infinite;\n  @keyframes donut-spin {\n    0% {\n      transform: rotate(0deg);\n    }\n    100% {\n      transform: rotate(360deg);\n    }\n  }\n"]);return x=function(){return e},e}var O=g.a.div(x()),F=g.a.div(j()),M=function(e){return o.a.createElement(F,null,o.a.createElement(O,null))},z=n(8);function D(){var e=Object(p.a)(["\n  display: none; /* Hidden by default */\n  position: fixed; /* Stay in place */\n  z-index: 1; /* Sit on top */\n  left: 0;\n  top: 0;\n  width: 100%; /* Full width */\n  height: 100%; /* Full height */\n  overflow: auto; /* Enable scroll if needed */\n  background-color: rgb(0, 0, 0); /* Fallback color */\n  background-color: rgba(0, 0, 0, 0.4); /* Black w/ opacity */\n\n  /* Modal Content/Box */\n  .modal-content {\n    background-color: #fefefe;\n    margin: 20px auto; /* 15% from the top and centered */\n    padding: 20px;\n    border: 1px solid #888;\n    width: 90%; /* Could be more or less, depending on screen size */\n    @media (min-width: 992px) {\n      width: 40%; /* Could be more or less, depending on screen size */\n    }\n  }\n\n  .buttons {\n    display: flex;\n    justify-content: space-around;\n    align-items: center;\n    a {\n      width: 100%;\n      margin: 0 0 0 1rem;\n    }\n    button {\n      margin: 0;\n    }\n  }\n\n  /* The Close Button */\n  .close {\n    color: #aaa;\n    float: right;\n    font-size: 28px;\n    font-weight: bold;\n  }\n\n  .asterisk {\n    color: red;\n  }\n\n  .close:hover,\n  .close:focus {\n    color: black;\n    text-decoration: none;\n    cursor: pointer;\n  }\n  form {\n    label {\n      display: block;\n      input,\n      select {\n        margin-top: 0.5rem;\n      }\n    }\n  }\n"]);return D=function(){return e},e}function _(){var e=Object(p.a)(["\n  .block {\n    display: block;\n  }\n\n  .none {\n    display: none;\n  }\n"]);return _=function(){return e},e}f.a.defaults.xsrfCookieName="csrftoken",f.a.defaults.xsrfHeaderName="X-CSRFToken";var R=g.a.div(_()),q=g.a.div(D()),A=function(e){function t(){var e,n;Object(l.a)(this,t);for(var a=arguments.length,o=new Array(a),r=0;r<a;r++)o[r]=arguments[r];return(n=Object(s.a)(this,(e=Object(d.a)(t)).call.apply(e,[this].concat(o)))).state={regions:[],types:[],name:null,region:null,zip_code:null,province:null,city:null,address:null,type:null,showModal:!1,loading:!1,error:null,redirecting:!1},n.handleFormChange=function(e){n.setState(Object(z.a)({},e.target.name,e.target.value))},n.handleFormSubmit=function(e){e.preventDefault();var t=n.state,a=t.name,o=t.region,r=t.zip_code,i=t.province,l=t.city,c=t.address,s=t.type;r.length>4?window.alert("Zip Code must not exceed to 4 digits"):(n.setState({loading:!0,redirecting:!1}),f.a.post(S,{method:"post",name:a,region:o,zip_code:r,province:i,city:l,address:c,type:s,headers:{Accept:"application/json","Content-Type":"application/json"}}).then(function(e){n.setState({loading:!1,redirecting:!0});var t=e.data.id;window.location.replace("/receptionist/settings/medical_institution/connect?id=".concat(t))}).catch(function(e){console.log(e),n.setState({loading:!1,error:e.response})}))},n}return Object(m.a)(t,e),Object(c.a)(t,[{key:"componentDidMount",value:function(){var e=this;f.a.get(y).then(function(t){var n=t.data.map(function(e){return e});e.setState({regions:n})}),f.a.get(E).then(function(t){var n=t.data.map(function(e){return e});e.setState({types:n})})}},{key:"render",value:function(){var e=this.state,t=e.regions,n=e.types,a=e.loading,r=e.error,i=e.redirecting,l=this.props,c=l.show,s=l.closeModalRef,d=l.regionSelectedF,m=l.regionID,u=l.provinces,p=l.provID,h=l.cities,f=l.provinceSelectedF,g=l.citySelectedF,v=t.map(function(e){var t=e.name,n=e.id;return o.a.createElement("option",{value:n,key:n},t)}),b=n.map(function(e){var t=e.name,n=e.id;return o.a.createElement("option",{value:n,key:n},t)}),y=u.map(function(e){var t=e.id,n=e.name;return o.a.createElement("option",{value:t,key:t},n)}),E=h.map(function(e){var t=e.id,n=e.name;return o.a.createElement("option",{value:t,key:t},n)});return o.a.createElement(R,null,o.a.createElement(q,{className:c?"block":"none"},o.a.createElement("div",{className:"modal-content"},o.a.createElement("span",{onClick:s,className:"close"},"\xd7"),o.a.createElement("form",{action:"POST",onChange:this.handleFormChange,onSubmit:this.handleFormSubmit},o.a.createElement("h4",{className:"text-center"},"Add Medical Institution"),o.a.createElement("div",{className:"form-group"},o.a.createElement("label",{htmlFor:"name"},"Name ",o.a.createElement("span",{className:"asterisk"},"*"),o.a.createElement("input",{className:"form-control",type:"text",name:"name",required:!0})),o.a.createElement("label",{htmlFor:"type"},"Type ",o.a.createElement("span",{className:"asterisk"},"*"),o.a.createElement("select",{className:"form-control",name:"type",required:!0},o.a.createElement("option",{defaultValue:!0},"Select Type"),b||"No options found")),o.a.createElement("label",{htmlFor:"region"},"Region ",o.a.createElement("span",{className:"asterisk"},"*"),o.a.createElement("select",{onChange:d,value:this.state.selected,className:"form-control",name:"region",required:!0},o.a.createElement("option",{defaultValue:!0},"Select Region"),v||"No options found")),m?o.a.createElement("label",{htmlFor:"province"},"Province ",o.a.createElement("span",{className:"asterisk"},"*"),o.a.createElement("select",{className:"form-control",name:"province",onChange:f,required:!0},o.a.createElement("option",{defaultValue:!0},"Select Province"),y||"null")):o.a.createElement("label",{htmlFor:"province"},"Province ",o.a.createElement("span",{className:"asterisk"},"*"),o.a.createElement("select",{className:"form-control",name:"province",onChange:f,required:!0},o.a.createElement("option",{defaultValue:!0},"Select Province"))),p?o.a.createElement("label",{htmlFor:"city"},"City ",o.a.createElement("span",{className:"asterisk"},"*"),o.a.createElement("select",{className:"form-control",name:"city",onChange:g,required:!0},o.a.createElement("option",{defaultValue:!0},"Select City"),E||"null")):o.a.createElement("label",{htmlFor:"city"},"City ",o.a.createElement("span",{className:"asterisk"},"*"),o.a.createElement("select",{required:!0,className:"form-control",name:"city",onChange:g},o.a.createElement("option",{defaultValue:!0},"Select City"))),o.a.createElement("label",{htmlFor:"address"},"Address ",o.a.createElement("span",{className:"asterisk"},"*"),o.a.createElement("input",{className:"form-control",type:"text",name:"address",required:!0})),o.a.createElement("label",{htmlFor:"zip_code"},"Zipcode",o.a.createElement("input",{className:"form-control",type:"number",name:"zip_code"}))),r?o.a.createElement("p",{className:"text-center",style:{color:"red",fontSize:"0.9em"}},r.data):null,o.a.createElement("div",{className:"buttons btn-group"},a?o.a.createElement("button",{type:"submit",className:"btn btn-primary btn-block",disabled:!0},"Submitting"):i?o.a.createElement("button",{type:"submit",className:"btn btn-primary btn-block",disabled:!0},"Redirecting"):o.a.createElement("button",{type:"submit",className:"btn btn-primary btn-block"},"Submit"),o.a.createElement("a",{href:"javascript:void(0)",onClick:s,className:"btn btn-block btn-secondary"},"Cancel"))))))}}]),t}(a.Component),V=n(420),I=n(423),B=n(419),P=n(422);function T(){var e=Object(p.a)(['\n  display: none; /* Hidden by default */\n  position: fixed; /* Stay in place */\n  z-index: 1; /* Sit on top */\n  left: 0;\n  top: 0;\n  width: 100%; /* Full width */\n  height: 100%; /* Full height */\n  overflow: auto; /* Enable scroll if needed */\n  background-color: rgb(0, 0, 0); /* Fallback color */\n  background-color: rgba(0, 0, 0, 0.4); /* Black w/ opacity */\n  p {\n    span {\n      font-weight: 600;\n    }\n  }\n  h5 {\n    text-align: center;\n  }\n  .leaflet-container {\n    height: 400px;\n    width: 100%;\n    margin: 0 auto;\n    overflow: hidden;\n  }\n\n  .details {\n    margin-top: 1rem;\n    label {\n      font-weight: 600;\n      small {\n        span {\n          &::after {\n            content: " ";\n          }\n        }\n      }\n    }\n  }\n\n  .buttons {\n    display: flex;\n    justify-content: space-around;\n    align-items: center;\n    a {\n      width: 100%;\n      &:first-of-type {\n        margin-right: 1rem;\n      }\n    }\n  }\n\n  /* Modal Content/Box */\n  .modal-content {\n    background-color: #fefefe;\n    margin: 20px auto; /* 15% from the top and centered */\n    padding: 20px;\n    border: 1px solid #888;\n    width: 90%; /* Could be more or less, depending on screen size */\n    @media (min-width: 992px) {\n      width: 40%; /* Could be more or less, depending on screen size */\n    }\n  }\n\n  /* The Close Button */\n  .close {\n    color: #aaa;\n    float: right;\n    font-size: 28px;\n    font-weight: bold;\n  }\n\n  .close:hover,\n  .close:focus {\n    color: black;\n    text-decoration: none;\n    cursor: pointer;\n  }\n  form {\n    label {\n      display: block;\n      input,\n      select {\n        margin-top: 0.5rem;\n      }\n    }\n  }\n']);return T=function(){return e},e}function H(){var e=Object(p.a)(["\n  .block {\n    display: block;\n  }\n\n  .none {\n    display: none;\n  }\n"]);return H=function(){return e},e}var J=g.a.div(H()),Q=g.a.div(T()),W=function(e){function t(){var e,n;Object(l.a)(this,t);for(var a=arguments.length,o=new Array(a),r=0;r<a;r++)o[r]=arguments[r];return(n=Object(s.a)(this,(e=Object(d.a)(t)).call.apply(e,[this].concat(o)))).state={zoom:19,showMap:!1},n}return Object(m.a)(t,e),Object(c.a)(t,[{key:"render",value:function(){var e=this.props,t=e.showDetails,n=e.details,a=e.closeDetailsModalRef,r=n.id,i=[];0===Object.keys(n.coordinates).length?i=[11.59,122.75]:i=[parseFloat(n.coordinates.lat),parseFloat(n.coordinates.lon)];return o.a.createElement(J,null,o.a.createElement(Q,{className:t?"block":"none"},o.a.createElement("div",{className:"modal-content"},o.a.createElement("span",{onClick:a,className:"close"},"\xd7"),0===Object.keys(n.coordinates).length?o.a.createElement("div",{style:{height:"400px",width:"100%",backgroundColor:"gray"}},o.a.createElement("p",{style:{textAlign:"center",color:"white"}},"No Location added on this institution")):o.a.createElement(V.a,{center:i,zoom:this.state.zoom},o.a.createElement(I.a,{attribution:'\xa9 <a href="https://osm.org/copyright">OpenStreetMap</a> contributors',url:"https://{s}.tile.osm.org/{z}/{x}/{y}.png"}),o.a.createElement(B.a,{position:i},o.a.createElement(P.a,null,"A pretty CSS3 popup. ",o.a.createElement("br",null)," Easily customizable."))),o.a.createElement("div",{className:"details"},o.a.createElement("h5",null,n.name," (",n.type,")"),o.a.createElement("label",null,"Address:"," ",o.a.createElement("small",null,o.a.createElement("span",null,""!==n.address?n.address:""),o.a.createElement("span",null,""!==n.city?n.city:""),o.a.createElement("span",null,""!==n.region?n.region:""),o.a.createElement("span",null,""!==n.zip_code?n.zip_code:""),o.a.createElement("span",null,""!==n.province?n.province:"")))),o.a.createElement("div",{className:"buttons"},o.a.createElement("a",{href:"".concat(b,"/receptionist/settings/medical_institution/connect?id=").concat(r),className:"btn btn-primary"},"Connect"),o.a.createElement("a",{href:"javascript:void(0)",className:"btn btn-secondary"},"More Details")))))}}]),t}(a.Component);function Z(){var e=Object(p.a)(["\n  margin: 0 0 1rem 0;\n  i {\n    font-size: 0.8em;\n  }\n"]);return Z=function(){return e},e}function L(){var e=Object(p.a)(["\n  display: flex;\n  flex-direction: row;\n  align-items: stretch;\n  ul {\n    width: 100%;\n    &:nth-child(1) {\n      flex: 1;\n      @media (min-width: 1200px) {\n        flex: 1;\n      }\n    }\n    &:nth-child(2) {\n      flex: 1;\n      .list-group-item {\n        text-align: center;\n        position: relative;\n        background-color: #469a27;\n        border: none;\n        margin: 0;\n        color: #fff;\n        /* border-radius: 0; */\n        i {\n          position: absolute;\n          left: 15px;\n          top: 17px;\n        }\n        &:hover {\n          background-color: #397c1f;\n        }\n      }\n    }\n  }\n"]);return L=function(){return e},e}function X(){var e=Object(p.a)(["\n  /* display: flex; */\n  flex-direction: column;\n  justify-content: center;\n  align-items: center;\n  select {\n    margin-bottom: 1rem;\n    option {\n      &:first-of-type {\n        color: rgba(0, 0, 0, 0.5);\n      }\n    }\n  }\n  input {\n    margin-bottom: 1rem;\n  }\n  p,\n  a {\n    margin-top: 1rem;\n  }\n"]);return X=function(){return e},e}var $=g.a.div(X()),G=g.a.div(L()),K=g.a.a(Z()),U=function(e){function t(){var e,n;Object(l.a)(this,t);for(var a=arguments.length,o=new Array(a),r=0;r<a;r++)o[r]=arguments[r];return(n=Object(s.a)(this,(e=Object(d.a)(t)).call.apply(e,[this].concat(o)))).state={addresses:[],searchResults:[],responseReceived:!1,provinces:[],regSelected:"",cities:[],provSelected:"",loading:!1,endpoint:k,queryString:{location:{name:null,id:0}},showModal:!1,showDetailsModal:!1,details:{name:null,type:null,address:null,region:null,province:null,city:null,zip_code:null,id:null,coordinates:[]}},n.handleChange=function(e){var t=Object(u.a)(Object(u.a)(n));if(""===e.target.value)n.setState({searchResults:[],responseReceived:!1});else if(e.target.value.length>=3){var a=k+"?"+n.makeQueryString(e.target.value);n.setState({loading:!0}),f.a.get(a).then(function(e){var n=e.data.map(function(e){return[e.id,e.name]});t.setState({loading:!1}),t.setState({responseReceived:!0}),t.setState({searchResults:n})}).catch(function(e){t.setState({responseReceived:!1}),console.log(e)}).then(function(){})}},n.regionSelected=function(e){n.setState({regSelected:e.target.value},function(){var e=n.state.regSelected,t=Object(u.a)(Object(u.a)(n));n.setState({cities:[]}),n.setState({queryString:{location:{name:"region",id:e}}}),n.setState({provinces:[],endpoint:"".concat(b,"/location/api/v1/provinces_of_region?region=").concat(e)}),f.a.get("".concat(b,"/location/api/v1/provinces_of_region?region=").concat(e)).then(function(e){var n=e.data.map(function(e){return e});t.setState({provinces:n})})})},n.provinceSelected=function(e){n.setState({provSelected:e.target.value},function(){var e=n.state.provSelected,t=Object(u.a)(Object(u.a)(n));n.setState({cities:[]}),n.setState({queryString:{location:{name:"province",id:e}}}),f.a.get("".concat(b,"/location/api/v1/cities_of_province?province=").concat(e)).then(function(e){var n=e.data.map(function(e){return e});t.setState({cities:n})})})},n.citySelected=function(e){n.setState({queryString:{location:{name:"city",id:e.target.value}}})},n.handleShowModal=function(){n.setState({showModal:!0})},n.handleCloseModal=function(){n.setState({showModal:!1})},n.handleShowDetailsModal=function(e){var t=Object(u.a)(Object(u.a)(n));f.a.get("".concat(b,"/doctor/api/v1/public/medical_institution/detail?id=").concat(e)).then(function(e){var n=e.data,a="",o=n.institution.name,r=n.institution.type.name,i="",l="",c="",s=n.institution.id;if(n.address[0]&&(a=n.address[0].address.address,i=n.address[0].address.region.name,l=n.address[0].address.province.name,c=n.address[0].address.zip_code),n.coordinates.length>0){var d=n.coordinates[0].coordinates;t.setState({details:{name:o,type:r,address:a,region:i,province:l,city:"",zip_code:c,id:s,coordinates:d}})}else t.setState({details:{name:o,type:r,address:a,region:i,province:l,city:"",zip_code:c,id:s,coordinates:[]}})}),n.setState({showDetailsModal:!0})},n.handleCloseDetailsModal=function(){n.setState({showDetailsModal:!1})},n}return Object(m.a)(t,e),Object(c.a)(t,[{key:"findMatches",value:function(e,t){return t.filter(function(t){var n=new RegExp(e,"gi");return t.name.match(n)})}},{key:"makeQueryString",value:function(e){var t="s="+e;return this.state.queryString.location.name&&(t=t+"&"+this.state.queryString.location.name+"="+this.state.queryString.location.id),t}},{key:"render",value:function(){var e,t=this,n=this.state.searchResults,a=this.state.loading;return e=n.map(function(e){return o.a.createElement(G,{key:e[0]},o.a.createElement("ul",{className:"list-group"},o.a.createElement("li",{className:"list-group-item"},o.a.createElement("a",{href:"javascript:void(0)",onClick:function(){return t.handleShowDetailsModal(e[0])}},e[1]))),o.a.createElement("ul",{className:"list-group"},o.a.createElement("a",{href:"".concat(b,"/receptionist/settings/medical_institution/connect?id=").concat(e[0]),className:"list-group-item"},o.a.createElement("i",{className:"fas fa-link"}),"Connect to this institution")))}),o.a.createElement(v.a,null,o.a.createElement($,{className:"container"},o.a.createElement(K,{className:"btn btn-success",href:"javascript:void(0)",onClick:this.handleShowModal},o.a.createElement("i",{className:"fas fa-plus"})," Add a new hospital or clinic"),o.a.createElement("input",{className:"form-control",onChange:this.handleChange,type:"text",placeholder:"Search..."}),o.a.createElement(C,{regionSelectedF:this.regionSelected,provinces:this.state.provinces,regionID:this.state.regSelected,provinceSelectedF:this.provinceSelected,cities:this.state.cities,provID:this.state.provSelected,citySelectedF:this.citySelected}),a?o.a.createElement(M,null):this.state.responseReceived?0===n.length?o.a.createElement("p",null,"No results found! "):e:o.a.createElement("p",null,"\xa0"),o.a.createElement(A,{show:this.state.showModal,closeModalRef:this.handleCloseModal,regionSelectedF:this.regionSelected,provinceSelectedF:this.provinceSelected,regionID:this.state.regSelected,provinces:this.state.provinces,cities:this.state.cities,provID:this.state.provSelected,citySelectedF:this.citySelected}),o.a.createElement(W,{showDetails:this.state.showDetailsModal,closeDetailsModalRef:this.handleCloseDetailsModal,details:this.state.details})))}}]),t}(a.Component);Boolean("localhost"===window.location.hostname||"[::1]"===window.location.hostname||window.location.hostname.match(/^127(?:\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}$/));i.a.render(o.a.createElement(U,null),document.getElementById("root")),"serviceWorker"in navigator&&navigator.serviceWorker.ready.then(function(e){e.unregister()})}},[[188,2,1]]]);
//# sourceMappingURL=main.a7b659b9.chunk.js.map