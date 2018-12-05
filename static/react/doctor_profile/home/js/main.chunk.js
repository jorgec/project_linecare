(window.webpackJsonp=window.webpackJsonp||[]).push([[0],{22:function(e,t,n){e.exports=n.p+"static/media/bg-01-01.611e88da.jpg"},23:function(e,t,n){e.exports=n.p+"static/media/profile-dummy.596d4987.png"},27:function(e,t,n){e.exports=n(57)},55:function(e,t,n){},57:function(e,t,n){"use strict";n.r(t);var a=n(0),o=n.n(a),r=n(5),l=n.n(r),c=n(17),i=n(18),d=n(24),s=n(19),m=n(25),u=n(1),p=n(4),f=n.n(p),h=n(2),v=function(e){return o.a.createElement("div",{className:"doctors-profile__container container"},e.children)};function g(){var e=Object(u.a)(["\n  background-color: rgba(0, 0, 0, 0.5);\n  height: 100%;\n  width: auto;\n  border-radius: 50%;\n  display: none;\n  transition: all 300ms ease-in;\n  justify-content: center;\n  align-items: center;\n  i {\n    color: #fff;\n    font-size: 1.2em;\n  }\n"]);return g=function(){return e},e}function b(){var e=Object(u.a)(["\n  height: 150px;\n  z-index: 499;\n  &:hover {\n    .profile-overlay {\n      display: flex;\n      cursor: pointer;\n    }\n  }\n"]);return b=function(){return e},e}var E=h.a.div(b()),y=h.a.div(g()),w=function(e){return o.a.createElement(E,{className:"doctors-profile__profile-photo",style:{backgroundImage:"url(".concat(e.profilePhoto,")")}},o.a.createElement(y,{onClick:e.openChangeProfilePhotoModal,className:"profile-overlay"},o.a.createElement("i",{className:"fas fa-camera fa-fw"})))},x=function(e){return o.a.createElement("div",{className:"doctors-profile__cover",style:{backgroundImage:"url(".concat(e.coverPhoto,")")}},o.a.createElement(w,{openChangeProfilePhotoModal:e.openChangeProfilePhotoModal,profilePhoto:e.profilePhoto}))};function P(){var e=Object(u.a)(["\n  height: ",";\n  width: ",";\n  background-color: #e2e2e2;\n  border-radius: 15px;\n"]);return P=function(){return e},e}var N=h.a.div(P(),function(e){return e.loaderHeight||"15px"},function(e){return e.loaderWidth||"50px"}),k=function(e){return o.a.createElement(N,{loaderWidth:e.loaderWidth,loaderHeight:e.loaderHeight})},_=function(e){var t,n=e.birthday;return t=new Date(Date.parse(n)).toDateString().replace(/^\S+\s/,""),o.a.createElement("div",{className:"col-lg-3"},o.a.createElement("div",{className:"doctors-profile__brief-info"},o.a.createElement("h6",{className:"h6"},"Brief Information"),n?o.a.createElement("p",null,t):o.a.createElement(k,{loaderHeight:"10px"})))},C=function(e){return o.a.createElement("div",{className:"col-lg-9"},o.a.createElement("div",{className:"doctors-profile__full-info"},o.a.createElement("h2",{className:"h2"},e.fullname?e.fullname:o.a.createElement(k,{loaderWidth:"500px"})),o.a.createElement("h6",{className:"h6"},e.abbreviation?"".concat(e.abbreviation," - ").concat(e.specialty):o.a.createElement(k,{loaderWidth:"200px"})),o.a.createElement("hr",null),o.a.createElement("div",{className:"tables"},o.a.createElement("table",{className:"table table-bordered"},o.a.createElement("thead",null,o.a.createElement("tr",null,o.a.createElement("th",{scope:"col"},"Hospital"),o.a.createElement("th",{scope:"col"},"Time"),o.a.createElement("th",{scope:"col"},"Queue"))),o.a.createElement("tbody",null,o.a.createElement("tr",null,o.a.createElement("td",null,"Mark"),o.a.createElement("td",null,"Otto"),o.a.createElement("td",null,"@mdo")),o.a.createElement("tr",null,o.a.createElement("td",null,"Jacob"),o.a.createElement("td",null,"Thornton"),o.a.createElement("td",null,"@fat")),o.a.createElement("tr",null,o.a.createElement("td",null,"Larry the Bird"),o.a.createElement("td",null,"@twitter"),o.a.createElement("td",null,"@twitter")))))))},O=function(e){var t=e.connections,n=[];t.forEach(function(e){n.push(e)});var a=n.map(function(e){return o.a.createElement("div",{className:"col-lg-4",key:e.id},o.a.createElement("div",{className:"item"},o.a.createElement("div",{className:"image",style:{backgroundImage:"url(".concat(e.profile_photo.photo,")")}}),o.a.createElement("div",{className:"info"},o.a.createElement("h6",{className:"h6"},"".concat(e.first_name," ").concat(e.last_name)),o.a.createElement("p",null,"Medical Field"))))});return o.a.createElement("div",{className:"col-lg-9"},o.a.createElement("div",{className:"connections__content"},o.a.createElement("h6",{className:"h6"},"Connections"),o.a.createElement("div",{className:"row"},a)))},j="";function M(){var e=Object(u.a)(["\n  padding: 2px 16px;\n  border-top: 1px solid rgba(0, 0, 0, 0.3);\n  color: #4a4a4a;\n"]);return M=function(){return e},e}function I(){var e=Object(u.a)(["\n  padding: 1rem 1rem;\n  display: flex;\n  flex-direction: column;\n  justify-content: center;\n  align-items: center;\n"]);return I=function(){return e},e}function S(){var e=Object(u.a)(["\n  padding: 1rem 16px;\n  border-bottom: 1px solid rgba(0, 0, 0, 0.3);\n  color: #4a4a4a;\n"]);return S=function(){return e},e}function D(){var e=Object(u.a)(["\n  position: relative;\n  background-color: #fefefe;\n  margin: auto;\n  padding: 0;\n  border: 1px solid #888;\n  width: 60%;\n  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);\n  -webkit-animation-name: animatetop;\n  -webkit-animation-duration: 0.4s;\n  animation-name: animatetop;\n  animation-duration: 0.4s;\n  /* Add Animation */\n  @-webkit-keyframes animatetop {\n    from {\n      top: -300px;\n      opacity: 0;\n    }\n    to {\n      top: 0;\n      opacity: 1;\n    }\n  }\n\n  @keyframes animatetop {\n    from {\n      top: -300px;\n      opacity: 0;\n    }\n    to {\n      top: 0;\n      opacity: 1;\n    }\n  }\n"]);return D=function(){return e},e}function F(){var e=Object(u.a)(["\n  display: ","; /* Hidden by default */\n  position: fixed; /* Stay in place */\n  z-index: 500; /* Sit on top */\n  padding-top: 200px; /* Location of the box */\n  left: 0;\n  top: 0;\n  width: 100%; /* Full width */\n  height: 100%; /* Full height */\n  overflow: auto; /* Enable scroll if needed */\n  background-color: rgb(0, 0, 0); /* Fallback color */\n  background-color: rgba(0, 0, 0, 0.4); /* Black w/ opacity */\n  .close {\n    color: rgba(0, 0, 0, 1);\n    float: right;\n    font-size: 28px;\n    font-weight: bold;\n  }\n\n  .close:hover,\n  .close:focus {\n    color: rgba(0, 0, 0, 0.4);\n    text-decoration: none;\n    cursor: pointer;\n  }\n"]);return F=function(){return e},e}var z=h.a.div(F(),function(e){return e.modalOpen?"block":"none"}),H=h.a.div(D()),W=h.a.div(S()),B=h.a.div(I()),A=h.a.div(M()),T=function(e){return o.a.createElement(z,{className:"modal",modalOpen:e.modalOpen},o.a.createElement(H,{className:"modal-content"},o.a.createElement(W,{className:"modal-header"},o.a.createElement("h5",{className:"h5"},e.title),o.a.createElement("span",{onClick:e.openChangeProfilePhotoModal,className:"close"},"\xd7")),o.a.createElement(B,{className:"modal-body"},e.children),o.a.createElement(A,{className:"modal-footer"})))},U=(n(55),n(22)),J=n.n(U),L=n(23),R=n.n(L);function Q(){var e=Object(u.a)(["\n  display: flex;\n  flex-direction: column;\n  justify-content: center;\n  align-items: center;\n  a {\n    margin-top: 1rem;\n  }\n"]);return Q=function(){return e},e}var X=h.a.div(Q());f.a.defaults.xsrfCookieName="csrftoken",f.a.defaults.xsrfHeaderName="X-CSRFToken";var $=function(e){function t(){var e,n;Object(c.a)(this,t);for(var a=arguments.length,o=new Array(a),r=0;r<a;r++)o[r]=arguments[r];return(n=Object(d.a)(this,(e=Object(s.a)(t)).call.apply(e,[this].concat(o)))).state={connections:[],doctorProfile:[],modalOpen:!1,uploadImg:""},n.openChangeProfilePhotoModal=function(){n.setState(function(e){return{modalOpen:!e.modalOpen}})},n.uploadProfilePhoto=function(){var e=n.state,t=e.uploadImg,a=e.doctorProfile,o={photo:t,caption:"".concat(a.full_name," Profile Photo")};f.a.post("".concat(j,"/album/api/private/upload?album=").concat(window.appContext.doctor_id),o,{headers:{"Content-Type":"multipart/form-data"}}).then(function(e){console.log(e)}).catch(function(e){console.log(e)})},n}return Object(m.a)(t,e),Object(i.a)(t,[{key:"getDoctorProfile",value:function(e){var t=this;f.a.get("".concat(j,"/doctor/api/v1/public/profile/detail?id=").concat(e)).then(function(e){console.log(e);var n=e.data;t.setState({doctorProfile:n})}).catch(function(e){console.log(e)})}},{key:"getDoctorConnections",value:function(e){var t=this;f.a.get("".concat(j,"/doctor/api/v1/private/medical_institution/receptionist/connected/list?doctor_id=").concat(e,"&fmt=full")).then(function(e){var n=e.data;t.setState({connections:n})}).catch(function(e){console.log(e)})}},{key:"componentDidMount",value:function(){this.getDoctorConnections(window.appContext.doctor_id),this.getDoctorProfile(window.appContext.doctor_id)}},{key:"previewUploadFile",value:function(e){var t=this,n="",a=e.target.files[0],o=new FileReader;o.onloadend=function(){n=o.result,t.setState({uploadImg:n})},a?o.readAsDataURL(a):(n="",this.setState({uploadImg:n}))}},{key:"render",value:function(){var e=this,t=this.state,n=t.connections,a=t.doctorProfile,r=t.uploadImg,l=null,c=null,i=null,d=null;return a.cover_photo&&(l=a.cover_photo.photo),a.profile_photo&&(c=a.profile_photo.photo),a.specializations&&(i=a.specializations[0].abbreviation,d=a.specializations[0].name),o.a.createElement(v,null,o.a.createElement(x,{coverPhoto:l||J.a,profilePhoto:c||R.a,openChangeProfilePhotoModal:this.openChangeProfilePhotoModal}),o.a.createElement("div",{className:"row"},o.a.createElement(_,{birthday:a.date_of_birth}),o.a.createElement(C,{fullname:a.full_name,abbreviation:i,specialty:d})),o.a.createElement(v,null,o.a.createElement("div",{className:"row"},o.a.createElement("div",{className:"offset-lg-3"}),o.a.createElement(O,{connections:n}))),o.a.createElement(T,{openChangeProfilePhotoModal:this.openChangeProfilePhotoModal,modalOpen:this.state.modalOpen},o.a.createElement("input",{type:"file",onChange:function(t){return e.previewUploadFile(t)}}),o.a.createElement("br",null),r?o.a.createElement(X,null,o.a.createElement("img",{src:r,height:"200",alt:"Preview..."}),o.a.createElement("a",{onClick:this.uploadProfilePhoto,className:"btn btn-primary",href:"javascript:void(0)"},"Upload")):null))}}]),t}(a.Component);Boolean("localhost"===window.location.hostname||"[::1]"===window.location.hostname||window.location.hostname.match(/^127(?:\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}$/));l.a.render(o.a.createElement($,null),document.getElementById("doctor_profile_app")),"serviceWorker"in navigator&&navigator.serviceWorker.ready.then(function(e){e.unregister()})}},[[27,2,1]]]);
//# sourceMappingURL=main.13e67023.chunk.js.map