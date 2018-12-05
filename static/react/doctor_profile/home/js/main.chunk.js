(window.webpackJsonp=window.webpackJsonp||[]).push([[0],{148:function(e,t,n){e.exports=n.p+"static/media/bg-01-01.611e88da.jpg"},149:function(e,t,n){e.exports=n.p+"static/media/profile-dummy.596d4987.png"},153:function(e,t,n){e.exports=n(385)},383:function(e,t,n){},385:function(e,t,n){"use strict";n.r(t);n(154);var o=n(1),a=n.n(o),r=n(70),i=n.n(r),l=n(143),c=n(144),s=n(150),d=n(145),m=n(151),p=n(26),u=n(34),f=n.n(u),h=function(e){return a.a.createElement("div",{className:"doctors-profile__container"},e.children)},v=n(11),g=n(12);function b(){var e=Object(v.a)(["\n  background-color: rgba(0, 0, 0, 0.5);\n  height: 100%;\n  width: auto;\n  border-radius: 50%;\n  display: none;\n  transition: all 300ms ease-in;\n  justify-content: center;\n  align-items: center;\n  i {\n    color: #fff;\n    font-size: 1.2em;\n  }\n"]);return b=function(){return e},e}function E(){var e=Object(v.a)(["\n  height: 150px;\n  z-index: 499;\n  &:hover {\n    .profile-overlay {\n      display: flex;\n      cursor: pointer;\n    }\n  }\n"]);return E=function(){return e},e}var P=g.a.div(E()),x=g.a.div(b()),y=function(e){return a.a.createElement(P,{className:"doctors-profile__profile-photo",style:{backgroundImage:"url(".concat(e.profilePhoto,")")}},a.a.createElement(x,{onClick:e.openChangeProfilePhotoModal,className:"profile-overlay"},a.a.createElement("i",{className:"fas fa-camera fa-fw"})))},w=function(e){return a.a.createElement("div",{className:"doctors-profile__cover",style:{backgroundImage:"url(".concat(e.coverPhoto,")")}},a.a.createElement("a",{href:"javascript:void(0)",onClick:e.openChangeCoverPhotoModal},"Change"),a.a.createElement(y,{openChangeProfilePhotoModal:e.openChangeProfilePhotoModal,profilePhoto:e.profilePhoto}))};function N(){var e=Object(v.a)(["\n  height: ",";\n  width: ",";\n  background-color: #e2e2e2;\n  border-radius: 15px;\n"]);return N=function(){return e},e}var k=g.a.div(N(),function(e){return e.loaderHeight||"15px"},function(e){return e.loaderWidth||"50px"}),C=function(e){return a.a.createElement(k,{loaderWidth:e.loaderWidth,loaderHeight:e.loaderHeight})},O=function(e){var t,n=e.birthday;return t=new Date(Date.parse(n)).toDateString().replace(/^\S+\s/,""),a.a.createElement("div",{className:"col-lg-3"},a.a.createElement("div",{className:"doctors-profile__brief-info"},a.a.createElement("h6",{className:"h6"},"Brief Information"),n?a.a.createElement("p",null,t):a.a.createElement(C,{loaderHeight:"10px"})))},_=function(e){return a.a.createElement("div",{className:"col-lg-9"},a.a.createElement("div",{className:"doctors-profile__full-info"},a.a.createElement("h2",{className:"h2"},e.fullname?e.fullname:a.a.createElement(C,{loaderWidth:"500px"})),a.a.createElement("h6",{className:"h6"},e.abbreviation?"".concat(e.abbreviation," - ").concat(e.specialty):a.a.createElement(C,{loaderWidth:"200px"})),a.a.createElement("hr",null),a.a.createElement("div",{className:"tables"},a.a.createElement("table",{className:"table table-bordered"},a.a.createElement("thead",null,a.a.createElement("tr",null,a.a.createElement("th",{scope:"col"},"Hospital"),a.a.createElement("th",{scope:"col"},"Time"),a.a.createElement("th",{scope:"col"},"Queue"))),a.a.createElement("tbody",null,a.a.createElement("tr",null,a.a.createElement("td",null,"Mark"),a.a.createElement("td",null,"Otto"),a.a.createElement("td",null,"@mdo")),a.a.createElement("tr",null,a.a.createElement("td",null,"Jacob"),a.a.createElement("td",null,"Thornton"),a.a.createElement("td",null,"@fat")),a.a.createElement("tr",null,a.a.createElement("td",null,"Larry the Bird"),a.a.createElement("td",null,"@twitter"),a.a.createElement("td",null,"@twitter")))))))},M="",j=function(e){var t,n,o=e.connections,r=[];o.forEach(function(e){t=e.connections[0].medical_institution.slug,n=e.connections[0].medical_institution.name,r.push(e)});var i=r.map(function(e){return a.a.createElement("div",{className:"col-lg-4",key:e.id},a.a.createElement("div",{className:"item"},a.a.createElement("div",{className:"image",style:{backgroundImage:"url(".concat(e.profile_photo.photo,")")}}),a.a.createElement("div",{className:"info"},a.a.createElement("h6",{className:"h6"},"".concat(e.first_name," ").concat(e.last_name)),a.a.createElement("a",{href:"".concat(M,"/doctor/medical_institution/").concat(t)},n))))});return a.a.createElement("div",{className:"col-lg-9"},a.a.createElement("div",{className:"connections__content"},a.a.createElement("h6",{className:"h6"},"Connections"),a.a.createElement("div",{className:"row"},i)))};function S(){var e=Object(v.a)(["\n  padding: 2px 16px;\n  border-top: 1px solid rgba(0, 0, 0, 0.3);\n  color: #4a4a4a;\n"]);return S=function(){return e},e}function A(){var e=Object(v.a)(["\n  padding: 1rem 1rem;\n  display: flex;\n  flex-direction: column;\n  justify-content: center;\n  align-items: center;\n"]);return A=function(){return e},e}function L(){var e=Object(v.a)(["\n  padding: 1rem 16px;\n  border-bottom: 1px solid rgba(0, 0, 0, 0.3);\n  color: #4a4a4a;\n"]);return L=function(){return e},e}function z(){var e=Object(v.a)(["\n  position: relative;\n  background-color: #fefefe;\n  margin: auto;\n  padding: 0;\n  border: 1px solid #888;\n  width: 60%;\n  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);\n  -webkit-animation-name: animatetop;\n  -webkit-animation-duration: 0.4s;\n  animation-name: animatetop;\n  animation-duration: 0.4s;\n  /* Add Animation */\n  @-webkit-keyframes animatetop {\n    from {\n      top: -300px;\n      opacity: 0;\n    }\n    to {\n      top: 0;\n      opacity: 1;\n    }\n  }\n\n  @keyframes animatetop {\n    from {\n      top: -300px;\n      opacity: 0;\n    }\n    to {\n      top: 0;\n      opacity: 1;\n    }\n  }\n"]);return z=function(){return e},e}function D(){var e=Object(v.a)(["\n  display: ","; /* Hidden by default */\n  position: fixed; /* Stay in place */\n  z-index: 500; /* Sit on top */\n  padding-top: 200px; /* Location of the box */\n  left: 0;\n  top: 0;\n  width: 100%; /* Full width */\n  height: 100%; /* Full height */\n  overflow: auto; /* Enable scroll if needed */\n  background-color: rgb(0, 0, 0); /* Fallback color */\n  background-color: rgba(0, 0, 0, 0.4); /* Black w/ opacity */\n  .close {\n    color: rgba(0, 0, 0, 1);\n    float: right;\n    font-size: 28px;\n    font-weight: bold;\n  }\n\n  .close:hover,\n  .close:focus {\n    color: rgba(0, 0, 0, 0.4);\n    text-decoration: none;\n    cursor: pointer;\n  }\n"]);return D=function(){return e},e}var H=g.a.div(D(),function(e){return e.profileModalOpen?"block":"none"}),F=g.a.div(z()),W=g.a.div(L()),B=g.a.div(A()),I=g.a.div(S()),T=function(e){return a.a.createElement(H,{className:"modal",profileModalOpen:e.profileModalOpen},a.a.createElement(F,{className:"modal-content"},a.a.createElement(W,{className:"modal-header"},a.a.createElement("h5",{className:"h5"},e.title),a.a.createElement("span",{onClick:e.openChangeProfilePhotoModal,className:"close"},"\xd7")),a.a.createElement(B,{className:"modal-body"},e.children),a.a.createElement(I,{className:"modal-footer"})))};function J(){var e=Object(v.a)(["\n  padding: 2px 16px;\n  border-top: 1px solid rgba(0, 0, 0, 0.3);\n  color: #4a4a4a;\n"]);return J=function(){return e},e}function Q(){var e=Object(v.a)(["\n  padding: 1rem 1rem;\n  display: flex;\n  flex-direction: column;\n  justify-content: center;\n  align-items: center;\n"]);return Q=function(){return e},e}function R(){var e=Object(v.a)(["\n  padding: 1rem 16px;\n  border-bottom: 1px solid rgba(0, 0, 0, 0.3);\n  color: #4a4a4a;\n"]);return R=function(){return e},e}function X(){var e=Object(v.a)(["\n  position: relative;\n  background-color: #fefefe;\n  margin: auto;\n  padding: 0;\n  border: 1px solid #888;\n  width: 60%;\n  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);\n  -webkit-animation-name: animatetop;\n  -webkit-animation-duration: 0.4s;\n  animation-name: animatetop;\n  animation-duration: 0.4s;\n  /* Add Animation */\n  @-webkit-keyframes animatetop {\n    from {\n      top: -300px;\n      opacity: 0;\n    }\n    to {\n      top: 0;\n      opacity: 1;\n    }\n  }\n\n  @keyframes animatetop {\n    from {\n      top: -300px;\n      opacity: 0;\n    }\n    to {\n      top: 0;\n      opacity: 1;\n    }\n  }\n"]);return X=function(){return e},e}function $(){var e=Object(v.a)(["\n  display: ","; /* Hidden by default */\n  position: fixed; /* Stay in place */\n  z-index: 500; /* Sit on top */\n  padding-top: 200px; /* Location of the box */\n  left: 0;\n  top: 0;\n  width: 100%; /* Full width */\n  height: 100%; /* Full height */\n  overflow: auto; /* Enable scroll if needed */\n  background-color: rgb(0, 0, 0); /* Fallback color */\n  background-color: rgba(0, 0, 0, 0.4); /* Black w/ opacity */\n  .close {\n    color: rgba(0, 0, 0, 1);\n    float: right;\n    font-size: 28px;\n    font-weight: bold;\n  }\n\n  .close:hover,\n  .close:focus {\n    color: rgba(0, 0, 0, 0.4);\n    text-decoration: none;\n    cursor: pointer;\n  }\n"]);return $=function(){return e},e}var q=g.a.div($(),function(e){return e.coverModalOpen?"block":"none"}),G=g.a.div(X()),K=g.a.div(R()),U=g.a.div(Q()),V=g.a.div(J()),Y=function(e){return a.a.createElement(q,{className:"modal",coverModalOpen:e.coverModalOpen},a.a.createElement(G,{className:"modal-content"},a.a.createElement(K,{className:"modal-header"},a.a.createElement("h5",{className:"h5"},e.title),a.a.createElement("span",{onClick:e.openChangeCoverPhotoModal,className:"close"},"\xd7")),a.a.createElement(U,{className:"modal-body"},e.children),a.a.createElement(V,{className:"modal-footer"})))},Z=(n(383),n(148)),ee=n.n(Z),te=n(149),ne=n.n(te);f.a.defaults.xsrfCookieName="csrftoken",f.a.defaults.xsrfHeaderName="X-CSRFToken";var oe=function(e){function t(){var e,n;Object(l.a)(this,t);for(var o=arguments.length,a=new Array(o),r=0;r<o;r++)a[r]=arguments[r];return(n=Object(s.a)(this,(e=Object(d.a)(t)).call.apply(e,[this].concat(a)))).state={connections:[],doctorProfile:[],profileModalOpen:!1,coverModalOpen:!1,profilePhoto:null,coverPhoto:null,profilePhotos:{id:null,photo:null},coverPhotos:{id:null,photo:null}},n.openChangeProfilePhotoModal=function(){n.setState(function(e){return{profileModalOpen:!e.profileModalOpen}})},n.openChangeCoverPhotoModal=function(){n.setState(function(e){return{coverModalOpen:!e.coverModalOpen}})},n.getProfileList=function(){var e=Object(p.a)(Object(p.a)(n));f.a.get("".concat(M,"/album/api/public/album/photos/all?id=").concat(window.appContext.profile_photo_album_id)).then(function(t){var n=t.data.map(function(e){return{photo:e.photo,id:e.id}});e.setState({profilePhotos:n})}).catch(function(e){console.log(e)})},n.getCoverList=function(){var e=Object(p.a)(Object(p.a)(n));f.a.get("".concat(M,"/album/api/public/album/photos/all?id=").concat(window.appContext.cover_photo_album_id)).then(function(t){var n=t.data.map(function(e){return{photo:e.photo,id:e.id}});e.setState({coverPhotos:n})}).catch(function(e){console.log(e)})},n.setAsProfilePhoto=function(e){var t=e.target.id,o=e.target.src,a=Object(p.a)(Object(p.a)(n));f.a.post("".concat(M,"/album/api/private/photo/set_primary?photo=").concat(t),{method:"POST"}).then(function(e){e&&a.setState({profilePhoto:o})}).catch(function(e){console.log(e)})},n.setAsCoverPhoto=function(e){var t=e.target.id,o=e.target.src,a=Object(p.a)(Object(p.a)(n));f.a.post("".concat(M,"/album/api/private/photo/set_primary?photo=").concat(t),{method:"POST"}).then(function(e){e&&a.setState({coverPhoto:o})}).catch(function(e){console.log(e)})},n}return Object(m.a)(t,e),Object(c.a)(t,[{key:"componentDidMount",value:function(){this.getDoctorConnections(window.appContext.doctor_id),this.getDoctorProfile(window.appContext.doctor_id),this.getProfileList(),this.getCoverList()}},{key:"getDoctorProfile",value:function(e){var t=this;f.a.get("".concat(M,"/doctor/api/v1/public/profile/detail?id=").concat(e)).then(function(e){var n=e.data,o=n.profile_photo.photo;t.setState({doctorProfile:n,profilePhoto:o})}).catch(function(e){console.log(e)})}},{key:"getDoctorConnections",value:function(e){var t=this;f.a.get("".concat(M,"/doctor/api/v1/private/medical_institution/receptionist/connected/list?doctor_id=").concat(e,"&fmt=full")).then(function(e){var n=e.data;t.setState({connections:n})}).catch(function(e){console.log(e)})}},{key:"render",value:function(){var e=this,t=this.state,n=t.connections,o=t.doctorProfile,r=t.profilePhotos,i=t.profilePhoto,l=t.coverPhoto,c=t.coverPhotos,s=null,d=null;o.specializations&&(s=o.specializations[0].abbreviation,d=o.specializations[0].name);var m=Array.from(r).map(function(t){return a.a.createElement("div",{className:"col-lg-3",key:t.id},a.a.createElement("a",{href:"javascript:void(0)",onClick:e.setAsProfilePhoto},a.a.createElement("img",{className:"img-fluid img-thumbnail",id:t.id,src:t.photo,alt:""})))}),p=Array.from(c).map(function(t){return a.a.createElement("div",{className:"col-lg-3",key:t.id},a.a.createElement("a",{href:"javascript:void(0)",onClick:e.setAsCoverPhoto},a.a.createElement("img",{className:"img-fluid img-thumbnail",id:t.id,src:t.photo,alt:""})))});return a.a.createElement(h,null,o?a.a.createElement("div",null,a.a.createElement(w,{coverPhoto:l||ee.a,profilePhoto:i||ne.a,openChangeProfilePhotoModal:this.openChangeProfilePhotoModal,openChangeCoverPhotoModal:this.openChangeCoverPhotoModal}),a.a.createElement("div",{className:"row"},a.a.createElement(O,{birthday:o.date_of_birth}),a.a.createElement(_,{fullname:o.full_name,abbreviation:s,specialty:d})),a.a.createElement(h,null,a.a.createElement("div",{className:"row"},a.a.createElement("div",{className:"offset-lg-3"}),a.a.createElement(j,{connections:n}))),a.a.createElement(T,{openChangeProfilePhotoModal:this.openChangeProfilePhotoModal,profileModalOpen:this.state.profileModalOpen,title:"Profile Lists"},a.a.createElement("div",{className:"row",id:"profileList"},m)),a.a.createElement(Y,{openChangeCoverPhotoModal:this.openChangeCoverPhotoModal,coverModalOpen:this.state.coverModalOpen,title:"Cover Lists"},a.a.createElement("div",{className:"row",id:"profileList"},p))):a.a.createElement("p",{style:{color:"red"}},"No Doctor Profile yet"))}}]),t}(o.Component);Boolean("localhost"===window.location.hostname||"[::1]"===window.location.hostname||window.location.hostname.match(/^127(?:\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}$/));i.a.render(a.a.createElement(oe,null),document.getElementById("doctor_profile_app")),"serviceWorker"in navigator&&navigator.serviceWorker.ready.then(function(e){e.unregister()})}},[[153,2,1]]]);
//# sourceMappingURL=main.ad36bb9a.chunk.js.map