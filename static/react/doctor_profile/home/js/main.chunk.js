(window.webpackJsonp=window.webpackJsonp||[]).push([[0],{157:function(e,n,t){e.exports=t.p+"static/media/bg-01-01.611e88da.jpg"},158:function(e,n,t){e.exports=t.p+"static/media/profile-dummy.596d4987.png"},162:function(e,n,t){e.exports=t(404)},402:function(e,n,t){},404:function(e,n,t){"use strict";t.r(n);t(163);var o=t(0),a=t.n(o),r=t(58),i=t.n(r),l=t(152),c=t(153),s=t(160),d=t(154),p=t(159),u=t(26),m=t(6),f=t(34),h=t.n(f),g=t(7),v=t(49),b=(t(398),function(e){return a.a.createElement("div",{className:"doctors-profile__container"},e.children)});function E(){var e=Object(m.a)(["\n  background-color: rgba(0, 0, 0, 0.5);\n  height: 100%;\n  width: auto;\n  border-radius: 50%;\n  display: none;\n  transition: all 300ms ease-in;\n  justify-content: center;\n  align-items: center;\n  i {\n    color: #fff;\n    font-size: 1.2em;\n  }\n"]);return E=function(){return e},e}function x(){var e=Object(m.a)(["\n  height: 150px;\n  z-index: 499;\n  &:hover {\n    .profile-overlay {\n      display: flex;\n      cursor: pointer;\n    }\n  }\n"]);return x=function(){return e},e}var y=g.a.div(x()),P=g.a.div(E()),k=function(e){return a.a.createElement(y,{className:"doctors-profile__profile-photo",style:{backgroundImage:"url(".concat(e.profilePhoto,")")}},a.a.createElement(P,{onClick:e.openChangeProfilePhotoModal,className:"profile-overlay"},a.a.createElement("i",{className:"fas fa-camera fa-fw"})))};function C(){var e=Object(m.a)(["\n  background-color: rgba(0, 0, 0, 0.1);\n  padding: 5px 10px;\n  position: absolute;\n  top: 5px;\n  left: 30px;\n  display: none;\n  color: rgba(255, 255, 255, 0.5);\n  &:hover {\n    background-color: rgba(0, 0, 0, 0.6);\n    color: #fff;\n    text-decoration: none;\n  }\n"]);return C=function(){return e},e}var w=g.a.a(C()),O=function(e){return a.a.createElement("div",{className:"doctors-profile__cover",style:{backgroundImage:"url(".concat(e.coverPhoto,")")}},a.a.createElement(w,{className:"show-edit-cover-button",href:"javascript:void(0)",onClick:e.openChangeCoverPhotoModal},"Change Cover Photo"),a.a.createElement(k,{openChangeProfilePhotoModal:e.openChangeProfilePhotoModal,profilePhoto:e.profilePhoto}))};function N(){var e=Object(m.a)(["\n  height: ",";\n  width: ",";\n  background-color: #e2e2e2;\n  border-radius: 15px;\n"]);return N=function(){return e},e}var j=g.a.div(N(),function(e){return e.loaderHeight||"15px"},function(e){return e.loaderWidth||"50px"}),_=function(e){return a.a.createElement(j,{loaderWidth:e.loaderWidth,loaderHeight:e.loaderHeight})},M=function(e){var n,t=e.birthday;return n=new Date(Date.parse(t)).toDateString().replace(/^\S+\s/,""),a.a.createElement("div",{className:"col-lg-3"},a.a.createElement("div",{className:"doctors-profile__brief-info"},a.a.createElement("h6",{className:"h6"},"Brief Information"),e.loadingData?a.a.createElement(_,{loaderHeight:"10px"}):t?a.a.createElement("p",null,n):a.a.createElement("p",{style:{fontStyle:"italic",fontSize:"0.8em"}},"No information found")))},S="",D=function(e){return a.a.createElement("div",{className:"col-lg-9"},a.a.createElement("div",{className:"doctors-profile__full-info"},a.a.createElement("h2",{className:"h2"},e.fullname?e.fullname:a.a.createElement(_,{loaderWidth:"500px"})),e.loadingData?a.a.createElement(_,{loaderWidth:"200px"}):e.abbreviation&&e.specialty?a.a.createElement("h6",{className:"h6"},e.specialty," - ",e.abbreviation):a.a.createElement("p",{style:{fontStyle:"italic"}},"Your doctor profile is incomplete."," ",a.a.createElement("a",{href:"".concat(S,"/doctor/settings")},"Click here to complete your settings.")),a.a.createElement("hr",null),a.a.createElement("div",{className:"tables"},a.a.createElement("table",{className:"table table-bordered"},a.a.createElement("thead",null,a.a.createElement("tr",null,a.a.createElement("th",{scope:"col"},"Hospital"),a.a.createElement("th",{scope:"col"},"Time"),a.a.createElement("th",{scope:"col"},"Queue"))),a.a.createElement("tbody",null,a.a.createElement("tr",null,a.a.createElement("td",null,"Mark"),a.a.createElement("td",null,"Otto"),a.a.createElement("td",null,"@mdo")),a.a.createElement("tr",null,a.a.createElement("td",null,"Jacob"),a.a.createElement("td",null,"Thornton"),a.a.createElement("td",null,"@fat")),a.a.createElement("tr",null,a.a.createElement("td",null,"Larry the Bird"),a.a.createElement("td",null,"@twitter"),a.a.createElement("td",null,"@twitter")))))))},z=function(e){var n=e.connections,t=[];n.forEach(function(e){t.push(e)});var o=t.map(function(e){return a.a.createElement("div",{className:"col-lg-4",key:e.id},a.a.createElement("div",{className:"item"},a.a.createElement("div",{className:"image",style:{backgroundImage:"url(".concat(e.profile_photo.photo,")")}}),a.a.createElement("div",{className:"info"},a.a.createElement("h6",{className:"h6"},"".concat(e.first_name," ").concat(e.last_name)),a.a.createElement("a",{href:"".concat(S,"/doctor/medical_institution/").concat(e.connections[0].medical_institution.slug)},e.connections[0].medical_institution.name))))});return a.a.createElement("div",{className:"col-lg-9"},a.a.createElement("div",{className:"connections__content"},a.a.createElement("h6",{className:"h6"},"Receptionists"),a.a.createElement("div",{className:"row"},t.length>0?o:a.a.createElement("div",{className:"col-lg-4"},a.a.createElement("p",{style:{fontStyle:"italic",fontSize:"0.8em"}},"You have no receptionists")))))};function H(){var e=Object(m.a)(["\n  padding: 2px 16px;\n  border-top: 1px solid rgba(0, 0, 0, 0.3);\n  color: #4a4a4a;\n"]);return H=function(){return e},e}function A(){var e=Object(m.a)(["\n  padding: 1rem 1rem;\n  display: flex;\n  flex-direction: column;\n  justify-content: center;\n  align-items: center;\n"]);return A=function(){return e},e}function B(){var e=Object(m.a)(["\n  padding: 1rem 16px;\n  border-bottom: 1px solid rgba(0, 0, 0, 0.3);\n  color: #4a4a4a;\n"]);return B=function(){return e},e}function F(){var e=Object(m.a)(["\n  position: relative;\n  background-color: #fefefe;\n  margin: auto;\n  padding: 0;\n  border: 1px solid #888;\n  width: 60%;\n  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);\n  -webkit-animation-name: animatetop;\n  -webkit-animation-duration: 0.4s;\n  animation-name: animatetop;\n  animation-duration: 0.4s;\n  /* Add Animation */\n  @-webkit-keyframes animatetop {\n    from {\n      top: -300px;\n      opacity: 0;\n    }\n    to {\n      top: 0;\n      opacity: 1;\n    }\n  }\n\n  @keyframes animatetop {\n    from {\n      top: -300px;\n      opacity: 0;\n    }\n    to {\n      top: 0;\n      opacity: 1;\n    }\n  }\n"]);return F=function(){return e},e}function L(){var e=Object(m.a)(["\n  display: ","; /* Hidden by default */\n  position: fixed; /* Stay in place */\n  z-index: 500; /* Sit on top */\n  padding-top: 200px; /* Location of the box */\n  left: 0;\n  top: 0;\n  width: 100%; /* Full width */\n  height: 100%; /* Full height */\n  overflow: auto; /* Enable scroll if needed */\n  background-color: rgb(0, 0, 0); /* Fallback color */\n  background-color: rgba(0, 0, 0, 0.4); /* Black w/ opacity */\n  .close {\n    color: rgba(0, 0, 0, 1);\n    float: right;\n    font-size: 28px;\n    font-weight: bold;\n  }\n\n  .close:hover,\n  .close:focus {\n    color: rgba(0, 0, 0, 0.4);\n    text-decoration: none;\n    cursor: pointer;\n  }\n"]);return L=function(){return e},e}var T=g.a.div(L(),function(e){return e.profileModalOpen?"block":"none"}),I=g.a.div(F()),W=g.a.div(B()),J=g.a.div(A()),R=g.a.div(H()),Y=function(e){return a.a.createElement(T,{className:"modal",profileModalOpen:e.profileModalOpen},a.a.createElement(I,{className:"modal-content"},a.a.createElement(W,{className:"modal-header"},a.a.createElement("h5",{className:"h5"},e.title),a.a.createElement("span",{onClick:e.openChangeProfilePhotoModal,className:"close"},"\xd7")),a.a.createElement(J,{className:"modal-body"},e.children),a.a.createElement(R,{className:"modal-footer"})))};function Q(){var e=Object(m.a)(["\n  padding: 2px 16px;\n  border-top: 1px solid rgba(0, 0, 0, 0.3);\n  color: #4a4a4a;\n"]);return Q=function(){return e},e}function V(){var e=Object(m.a)(["\n  padding: 1rem 1rem;\n  display: flex;\n  flex-direction: column;\n  justify-content: center;\n  align-items: center;\n"]);return V=function(){return e},e}function X(){var e=Object(m.a)(["\n  padding: 1rem 16px;\n  border-bottom: 1px solid rgba(0, 0, 0, 0.3);\n  color: #4a4a4a;\n"]);return X=function(){return e},e}function $(){var e=Object(m.a)(["\n  position: relative;\n  background-color: #fefefe;\n  margin: auto;\n  padding: 0;\n  border: 1px solid #888;\n  width: 60%;\n  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);\n  -webkit-animation-name: animatetop;\n  -webkit-animation-duration: 0.4s;\n  animation-name: animatetop;\n  animation-duration: 0.4s;\n  /* Add Animation */\n  @-webkit-keyframes animatetop {\n    from {\n      top: -300px;\n      opacity: 0;\n    }\n    to {\n      top: 0;\n      opacity: 1;\n    }\n  }\n\n  @keyframes animatetop {\n    from {\n      top: -300px;\n      opacity: 0;\n    }\n    to {\n      top: 0;\n      opacity: 1;\n    }\n  }\n"]);return $=function(){return e},e}function q(){var e=Object(m.a)(["\n  display: ","; /* Hidden by default */\n  position: fixed; /* Stay in place */\n  z-index: 500; /* Sit on top */\n  padding-top: 200px; /* Location of the box */\n  left: 0;\n  top: 0;\n  width: 100%; /* Full width */\n  height: 100%; /* Full height */\n  overflow: auto; /* Enable scroll if needed */\n  background-color: rgb(0, 0, 0); /* Fallback color */\n  background-color: rgba(0, 0, 0, 0.4); /* Black w/ opacity */\n  .close {\n    color: rgba(0, 0, 0, 1);\n    float: right;\n    font-size: 28px;\n    font-weight: bold;\n  }\n\n  .close:hover,\n  .close:focus {\n    color: rgba(0, 0, 0, 0.4);\n    text-decoration: none;\n    cursor: pointer;\n  }\n"]);return q=function(){return e},e}var G=g.a.div(q(),function(e){return e.coverModalOpen?"block":"none"}),K=g.a.div($()),U=g.a.div(X()),Z=g.a.div(V()),ee=g.a.div(Q()),ne=function(e){return a.a.createElement(G,{className:"modal",coverModalOpen:e.coverModalOpen},a.a.createElement(K,{className:"modal-content"},a.a.createElement(U,{className:"modal-header"},a.a.createElement("h5",{className:"h5"},e.title),a.a.createElement("span",{onClick:e.openChangeCoverPhotoModal,className:"close"},"\xd7")),a.a.createElement(Z,{className:"modal-body"},e.children),a.a.createElement(ee,{className:"modal-footer"})))};function te(){var e=Object(m.a)(["\n  padding: 2px 16px;\n  color: #4a4a4a;\n"]);return te=function(){return e},e}function oe(){var e=Object(m.a)(["\n  padding: 1rem 1rem;\n  display: flex;\n  flex-direction: column;\n  justify-content: center;\n  align-items: center;\n"]);return oe=function(){return e},e}function ae(){var e=Object(m.a)(["\n  padding: 1rem 16px;\n  color: #4a4a4a;\n"]);return ae=function(){return e},e}function re(){var e=Object(m.a)(["\n  position: relative;\n  background-color: #fefefe;\n  margin: auto;\n  padding: 0;\n  width: 60%;\n  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);\n  -webkit-animation-name: animatetop;\n  -webkit-animation-duration: 0.4s;\n  animation-name: animatetop;\n  animation-duration: 0.4s;\n  /* Add Animation */\n  @-webkit-keyframes animatetop {\n    from {\n      top: -300px;\n      opacity: 0;\n    }\n    to {\n      top: 0;\n      opacity: 1;\n    }\n  }\n\n  @keyframes animatetop {\n    from {\n      top: -300px;\n      opacity: 0;\n    }\n    to {\n      top: 0;\n      opacity: 1;\n    }\n  }\n"]);return re=function(){return e},e}function ie(){var e=Object(m.a)(["\n  display: ","; /* Hidden by default */\n  position: fixed; /* Stay in place */\n  z-index: 500; /* Sit on top */\n  padding-top: 200px; /* Location of the box */\n  left: 0;\n  top: 0;\n  width: 100%; /* Full width */\n  height: 100%; /* Full height */\n  overflow: auto; /* Enable scroll if needed */\n  background-color: rgb(0, 0, 0); /* Fallback color */\n  background-color: rgba(0, 0, 0, 0.4); /* Black w/ opacity */\n  .close {\n    color: rgba(0, 0, 0, 1);\n    float: right;\n    font-size: 28px;\n    font-weight: bold;\n  }\n\n  .close:hover,\n  .close:focus {\n    color: rgba(0, 0, 0, 0.4);\n    text-decoration: none;\n    cursor: pointer;\n  }\n"]);return ie=function(){return e},e}var le=g.a.div(ie(),function(e){return e.loadingProfile?"block":"none"}),ce=g.a.div(re()),se=g.a.div(ae()),de=g.a.div(oe()),pe=g.a.div(te()),ue=function(e){return a.a.createElement(le,{className:"modal",loadingCover:e.loadingCover,loadingProfile:e.loadingProfile},a.a.createElement(ce,{className:"modal-content"},a.a.createElement(se,{className:"modal-header"}),a.a.createElement(de,{className:"modal-body"},e.loadingProfile?a.a.createElement("p",{className:"text-center"},e.error?e.error.message:"Setting profile..."):null),a.a.createElement(pe,{className:"modal-footer"})))},me=(t(402),t(157)),fe=t.n(me),he=t(158),ge=t.n(he);function ve(){var e=Object(m.a)(["\n  height: 150px;\n  min-width: 180px;\n  background-repeat: no-repeat;\n  background-color: gray;\n  background-position: center center;\n  background-size: cover;\n  margin-top: 1rem;\n"]);return ve=function(){return e},e}h.a.defaults.xsrfCookieName="csrftoken",h.a.defaults.xsrfHeaderName="X-CSRFToken";var be=g.a.div(ve()),Ee=function(e){function n(){var e,t;Object(l.a)(this,n);for(var o=arguments.length,a=new Array(o),r=0;r<o;r++)a[r]=arguments[r];return(t=Object(s.a)(this,(e=Object(d.a)(n)).call.apply(e,[this].concat(a)))).state={connections:[],doctorProfile:[],profileModalOpen:!1,coverModalOpen:!1,profilePhoto:null,coverPhoto:null,loadingProfile:!1,error:null,loadingData:!1,profilePhotos:{id:null,photo:null},coverPhotos:{id:null,photo:null}},t.successProfileChanged=function(){return v.toast.success("Profile photo changed!",{position:"top-right",autoClose:5e3,hideProgressBar:!0,closeOnClick:!0,pauseOnHover:!1,draggable:!1})},t.errorProfileChanged=function(e){return v.toast.error("".concat(e.message),{position:"top-right",autoClose:5e3,hideProgressBar:!0,closeOnClick:!0,pauseOnHover:!1,draggable:!1})},t.successCoverChanged=function(){return v.toast.success("Cover Photo changed!",{position:"top-right",autoClose:5e3,hideProgressBar:!0,closeOnClick:!0,pauseOnHover:!1,draggable:!1})},t.errorCoverChanged=function(e){return v.toast.error("".concat(e.message),{position:"top-right",autoClose:5e3,hideProgressBar:!0,closeOnClick:!0,pauseOnHover:!1,draggable:!1})},t.openChangeProfilePhotoModal=function(){t.setState(function(e){return{profileModalOpen:!e.profileModalOpen}})},t.openChangeCoverPhotoModal=function(){t.setState(function(e){return{coverModalOpen:!e.coverModalOpen}})},t.getProfileList=function(){var e=Object(u.a)(Object(u.a)(t));h.a.get("".concat(S,"/album/api/public/album/photos/all?id=").concat(window.appContext.profile_photo_album_id)).then(function(n){var t=n.data.map(function(e){return{photo:e.photo,id:e.id}});e.setState({profilePhotos:t})}).catch(function(e){console.log(e)})},t.getCoverList=function(){var e=Object(u.a)(Object(u.a)(t));h.a.get("".concat(S,"/album/api/public/album/photos/all?id=").concat(window.appContext.cover_photo_album_id)).then(function(n){var t=n.data.map(function(e){return{photo:e.photo,id:e.id}});e.setState({coverPhotos:t})}).catch(function(e){console.log(e)})},t.setAsProfilePhoto=function(e,n){var o=Object(u.a)(Object(u.a)(t));h.a.post("".concat(S,"/album/api/private/photo/set_primary?photo=").concat(e),{method:"POST"}).then(function(e){e&&(o.setState({profilePhoto:n}),o.successProfileChanged())}).catch(function(e){e&&(o.errorProfileChanged(e),setTimeout(function(){window.location.replace("".concat(S,"/doctor/home"))},2e3))})},t.setAsCoverPhoto=function(e,n){var o=Object(u.a)(Object(u.a)(t));h.a.post("".concat(S,"/album/api/private/photo/set_primary?photo=").concat(e),{method:"POST"}).then(function(e){e&&(o.setState({coverPhoto:n}),o.successCoverChanged())}).catch(function(e){e&&(o.errorCoverChanged(e),setTimeout(function(){window.location.replace("".concat(S,"/doctor/home"))},2e3))})},t}return Object(p.a)(n,e),Object(c.a)(n,[{key:"componentDidMount",value:function(){this.getDoctorConnections(window.appContext.doctor_id),this.getDoctorProfile(window.appContext.doctor_id),this.getProfileList(),this.getCoverList()}},{key:"getDoctorProfile",value:function(e){var n=this;this.setState({loadingData:!0}),h.a.get("".concat(S,"/doctor/api/v1/public/profile/detail?id=").concat(e)).then(function(e){var t=e.data,o=t.profile_photo.photo,a=t.cover_photo.photo;n.setState({doctorProfile:t,profilePhoto:o,coverPhoto:a,loadingData:!1})}).catch(function(e){console.log(e)})}},{key:"getDoctorConnections",value:function(e){var n=this;h.a.get("".concat(S,"/doctor/api/v1/private/medical_institution/receptionist/connected/list?doctor_id=").concat(e,"&fmt=full")).then(function(e){var t=e.data;n.setState({connections:t})}).catch(function(e){console.log(e)})}},{key:"render",value:function(){var e=this,n=this.state,t=n.connections,o=n.doctorProfile,r=n.profilePhotos,i=n.profilePhoto,l=n.coverPhoto,c=n.coverPhotos,s=n.loadingData,d=null,p=null;o.specializations?o.specializations.length>0&&(d=o.specializations[0].abbreviation,p=o.specializations[0].name):(d=null,p=null);var u=Array.from(r).map(function(n){return a.a.createElement("div",{key:n.id,className:r.length<4?"col-lg-4":"col-lg-3"},a.a.createElement("a",{href:"javascript:void(0)",onClick:function(t){return e.setAsProfilePhoto(n.id,n.photo)}},a.a.createElement(be,{style:{backgroundImage:"url(".concat(n.photo,")")},alt:""})))}),m=Array.from(c).map(function(n){return a.a.createElement("div",{key:n.id,className:c.length<4?"col-lg-4":"col-lg-3"},a.a.createElement("a",{href:"javascript:void(0)",onClick:function(t){return e.setAsCoverPhoto(n.id,n.photo)}},a.a.createElement(be,{style:{backgroundImage:"url(".concat(n.photo,")")},alt:""})))});return a.a.createElement(b,null,a.a.createElement(v.ToastContainer,{transition:v.Slide,position:"top-right",autoClose:5e3,hideProgressBar:!0,newestOnTop:!1,closeOnClick:!0,rtl:!1,pauseOnVisibilityChange:!0,draggable:!1,pauseOnHover:!1}),o?a.a.createElement("div",null,a.a.createElement(O,{coverPhoto:l||fe.a,profilePhoto:i||ge.a,openChangeProfilePhotoModal:this.openChangeProfilePhotoModal,openChangeCoverPhotoModal:this.openChangeCoverPhotoModal}),a.a.createElement("div",{className:"row"},a.a.createElement(M,{loadingData:s,birthday:o.date_of_birth}),a.a.createElement(D,{fullname:o.full_name,abbreviation:d,specialty:p,loadingData:s})),a.a.createElement(b,null,a.a.createElement("div",{className:"row"},a.a.createElement("div",{className:"offset-lg-3"}),a.a.createElement(z,{connections:t}))),a.a.createElement(Y,{openChangeProfilePhotoModal:this.openChangeProfilePhotoModal,profileModalOpen:this.state.profileModalOpen,title:"My Profile Photos"},a.a.createElement("div",{id:"profileList",className:"row"},u)),a.a.createElement(ne,{openChangeCoverPhotoModal:this.openChangeCoverPhotoModal,coverModalOpen:this.state.coverModalOpen,title:"My Cover Photos"},a.a.createElement("div",{id:"profileList",className:"row"},m)),a.a.createElement(ue,{error:this.state.error,loadingProfile:this.state.loadingProfile})):a.a.createElement("p",{style:{color:"red"}},"No Doctor Profile yet"))}}]),n}(o.Component);Boolean("localhost"===window.location.hostname||"[::1]"===window.location.hostname||window.location.hostname.match(/^127(?:\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}$/));i.a.render(a.a.createElement(Ee,null),document.getElementById("doctor_profile_app")),"serviceWorker"in navigator&&navigator.serviceWorker.ready.then(function(e){e.unregister()})}},[[162,2,1]]]);
//# sourceMappingURL=main.efb7edd2.chunk.js.map