(window.webpackJsonp=window.webpackJsonp||[]).push([[0],{40:function(e,t,n){e.exports=n(75)},75:function(e,t,n){"use strict";n.r(t);var a=n(1),r=n.n(a),c=n(17),o=n.n(c),i=n(19),s=n(9),l=n(11),p=n.n(l),u=n(16),m=n(3),d=n(4),h=n(6),f=n(5),b=n(7),v=function(e){function t(){return Object(m.a)(this,t),Object(h.a)(this,Object(f.a)(t).apply(this,arguments))}return Object(b.a)(t,e),Object(d.a)(t,[{key:"_handleSelectionChanged",value:function(e){var t=e.target.value;"---"!==t?this.props.dispatchSelectionChanged(t):this.props.dispatchSelectionChanged("")}},{key:"render",value:function(){return this.props.medical_institutions?r.a.createElement("select",{className:"form-control",onChange:this._handleSelectionChanged.bind(this)},r.a.createElement("option",null,"---"),this.props.medical_institutions.map(function(e){return r.a.createElement("option",{value:e.id,key:e.id},e.name)})):r.a.createElement("div",{className:"text-center"},r.a.createElement("div",{className:"donut-spinner"},"\xa0"))}}]),t}(a.Component),E=Object(s.b)(function(e){return{state:e}},function(e){return{dispatchSelectionChanged:function(t){return e({type:"UPDATE_PARAM",value:t,name:"medical_institution"})}}})(v),g=n(22),y=n.n(g),_=n(21),O=(n(34),function(e){function t(){var e,n;Object(m.a)(this,t);for(var a=arguments.length,r=new Array(a),c=0;c<a;c++)r[c]=arguments[c];return(n=Object(h.a)(this,(e=Object(f.a)(t)).call.apply(e,[this].concat(r))))._handleDateChanged=function(e){n.props.dispatchDateChanged(e.toISOString().split("T")[0])},n}return Object(b.a)(t,e),Object(d.a)(t,[{key:"render",value:function(){var e=new Date(this.props.state.day_start);return r.a.createElement(_.a,{className:"form-control",selected:e,onChange:this._handleDateChanged,dateFormat:"YYYY-MM-dd"})}}]),t}(a.Component)),j=Object(s.b)(function(e){return{state:e}},function(e){return{dispatchDateChanged:function(t){return e({type:"UPDATE_PARAM",value:t,name:"day_start"})}}})(O),C=function(e){function t(){var e,n;Object(m.a)(this,t);for(var a=arguments.length,r=new Array(a),c=0;c<a;c++)r[c]=arguments[c];return(n=Object(h.a)(this,(e=Object(f.a)(t)).call.apply(e,[this].concat(r))))._handleDateChanged=function(e){n.props.dispatchDateChanged(e.toISOString().split("T")[0])},n}return Object(b.a)(t,e),Object(d.a)(t,[{key:"render",value:function(){var e=new Date(this.props.state.day_end);return r.a.createElement(_.a,{className:"form-control",selected:e,onChange:this._handleDateChanged,dateFormat:"YYYY-MM-dd"})}}]),t}(a.Component),N=Object(s.b)(function(e){return{state:e}},function(e){return{dispatchDateChanged:function(t){return e({type:"UPDATE_PARAM",value:t,name:"day_end"})}}})(C),A="production",k={local:{baseURL:"http://linecare.local:8000"},testing:{baseURL:"https://192.168.10.220"},production_remote:{baseURL:"https://linecare.ph"},production:{baseURL:""}},w=k[A],S={checkup:"Check Up",followup:"Follow Up",lab_result:"Lab Result",consultation:"Consultation"},P=function(e){function t(){var e,n;Object(m.a)(this,t);for(var a=arguments.length,r=new Array(a),c=0;c<a;c++)r[c]=arguments[c];return(n=Object(h.a)(this,(e=Object(f.a)(t)).call.apply(e,[this].concat(r))))._handleSelectionChanged=function(e){var t=e.target.value;"---"!==t?n.props.dispatchSelectionChanged(t):n.props.dispatchSelectionChanged("")},n}return Object(b.a)(t,e),Object(d.a)(t,[{key:"render",value:function(){var e=[];return Object.keys(S).forEach(function(t){e.push(r.a.createElement("option",{value:t,key:t},S[t]))}),r.a.createElement("select",{className:"form-control",onChange:this._handleSelectionChanged},r.a.createElement("option",null,"---"),e)}}]),t}(a.Component),D=Object(s.b)(function(e){return{state:e}},function(e){return{dispatchSelectionChanged:function(t){return e({type:"UPDATE_PARAM",value:t,name:"appointment_type"})}}})(P),x={pending:"Pending",queueing:"Queueing",in_progress:"In Progress",finishing:"Finishing",done:"Done",cancelled_by_patient:"Cancelled by patient",cancelled_by_doctor:"Cancelled by doctor",rescheduled_by_patient:"Rescheduled by patient",rescheduled_by_doctor:"Rescheduled by doctor"},R=function(e){function t(){var e,n;Object(m.a)(this,t);for(var a=arguments.length,r=new Array(a),c=0;c<a;c++)r[c]=arguments[c];return(n=Object(h.a)(this,(e=Object(f.a)(t)).call.apply(e,[this].concat(r))))._handleSelectionChanged=function(e){var t=e.target.value;return"---"!==t?n.props.dispatchSelectionChanged(t):n.props.dispatchSelectionChanged(""),""},n}return Object(b.a)(t,e),Object(d.a)(t,[{key:"render",value:function(){var e=[];return Object.keys(x).forEach(function(t){e.push(r.a.createElement("option",{value:t,key:t},x[t]))}),r.a.createElement("select",{className:"form-control",onChange:this._handleSelectionChanged},r.a.createElement("option",null,"---"),e)}}]),t}(a.Component),U=Object(s.b)(function(e){return{state:e}},function(e){return{dispatchSelectionChanged:function(t){return e({type:"UPDATE_PARAM",value:t,name:"appointment_status"})}}})(R),I=function(e){function t(){var e,n;Object(m.a)(this,t);for(var a=arguments.length,r=new Array(a),c=0;c<a;c++)r[c]=arguments[c];return(n=Object(h.a)(this,(e=Object(f.a)(t)).call.apply(e,[this].concat(r))))._handleInput=function(e){var t=e.target.value;t.length>=3?n.props.dispatchTextChanged(t):n.props.dispatchTextChanged("")},n}return Object(b.a)(t,e),Object(d.a)(t,[{key:"render",value:function(){return r.a.createElement("input",{type:"text",className:"form-control",placeholder:"Search...",onInput:this._handleInput})}}]),t}(a.Component),T=Object(s.b)(function(e){return{state:e}},function(e){return{dispatchTextChanged:function(t){return e({type:"UPDATE_PARAM",value:t,name:"s"})}}})(I),M={10:"10",50:"50",100:"100"},L=function(e){function t(){var e,n;Object(m.a)(this,t);for(var a=arguments.length,r=new Array(a),c=0;c<a;c++)r[c]=arguments[c];return(n=Object(h.a)(this,(e=Object(f.a)(t)).call.apply(e,[this].concat(r))))._handleSelectionChanged=function(e){var t=e.target.value;"---"!==t?n.props.dispatchSelectionChanged(t):n.props.dispatchSelectionChanged("")},n}return Object(b.a)(t,e),Object(d.a)(t,[{key:"render",value:function(){var e=[];return Object.keys(M).forEach(function(t){e.push(r.a.createElement("option",{value:t,key:t},M[t]))}),r.a.createElement("select",{className:"form-control",onChange:this._handleSelectionChanged},r.a.createElement("option",null,"---"),e)}}]),t}(a.Component),F=Object(s.b)(function(e){return{state:e}},function(e){return{dispatchSelectionChanged:function(t){return e({type:"UPDATE_PARAM",value:t,name:"grab",cast:"int"})}}})(L);function Y(e){return"?"+Object.keys(e).map(function(t){return encodeURIComponent(t)+"="+encodeURIComponent(e[t])}).join("&")}var X=function(e){function t(){return Object(m.a)(this,t),Object(h.a)(this,Object(f.a)(t).apply(this,arguments))}return Object(b.a)(t,e),Object(d.a)(t,[{key:"render",value:function(){var e="".concat(k[A].baseURL,"/doctor/patients/appointment/detail?appointment=").concat(this.props.appointment.id),t="".concat(k[A].baseURL,"/doctor/schedule/").concat(this.props.appointment.medical_institution.slug,"/history?date=").concat(this.props.appointment.schedule_day.date_obj);return r.a.createElement("div",null,r.a.createElement("strong",null,this.props.appointment.type),r.a.createElement("br",null),r.a.createElement("a",{href:e},this.props.appointment.time_start.format_12," - ",this.props.appointment.time_end.format_12),r.a.createElement("br",null),r.a.createElement("small",null,r.a.createElement("a",{href:t},"".concat(this.props.appointment.schedule_day.day_name,",\n                 ").concat(this.props.appointment.schedule_day.month_name,"\n                 ").concat(this.props.appointment.schedule_day.day,",\n                 ").concat(this.props.appointment.schedule_day.year))))}}]),t}(a.Component),B=function(e){function t(){return Object(m.a)(this,t),Object(h.a)(this,Object(f.a)(t).apply(this,arguments))}return Object(b.a)(t,e),Object(d.a)(t,[{key:"render",value:function(){var e="".concat(k[A].baseURL,"/doctor/patients/").concat(this.props.appointment.patient.id,"/detail"),t="".concat(k[A].baseURL,"/doctor/medical_institution/").concat(this.props.appointment.medical_institution.slug);return r.a.createElement("div",null,r.a.createElement("a",{href:e},r.a.createElement("strong",null,this.props.appointment.patient.full_name)),r.a.createElement("br",null),r.a.createElement("a",{href:t},r.a.createElement("em",null,this.props.appointment.medical_institution.name)),r.a.createElement("br",null),r.a.createElement("small",null,this.props.appointment.medical_institution.address_text))}}]),t}(a.Component),J=function(e){function t(){return Object(m.a)(this,t),Object(h.a)(this,Object(f.a)(t).apply(this,arguments))}return Object(b.a)(t,e),Object(d.a)(t,[{key:"render",value:function(){return r.a.createElement("div",{className:"row no-gutters pb-1 mb-2 border-bottom border-secondary"},r.a.createElement("div",{className:"col-sm-3"},r.a.createElement(X,{appointment:this.props.appointment})),r.a.createElement("div",{className:"col-sm-7"},r.a.createElement(B,{appointment:this.props.appointment})),r.a.createElement("div",{className:"col-sm-2"},this.props.appointment.status_display))}}]),t}(a.Component),V=function(e){function t(){return Object(m.a)(this,t),Object(h.a)(this,Object(f.a)(t).apply(this,arguments))}return Object(b.a)(t,e),Object(d.a)(t,[{key:"render",value:function(){return void 0!==this.props.appointments?this.props.appointments.length>0?r.a.createElement("div",{className:"card"},r.a.createElement("div",{className:"card-header"},r.a.createElement("h4",{className:"card-title"},"Appointments ",r.a.createElement("small",{className:"float-right badge badge-secondary"},this.props.appointments.length))),r.a.createElement("div",{className:"card-body"},this.props.appointments.map(function(e){return r.a.createElement(J,{key:e.id,appointment:e})}))):r.a.createElement("div",{className:"alert alert-danger"},"No appointments matched your filters"):r.a.createElement("div",{className:"text-center"},r.a.createElement("div",{className:"donut-spinner"},"\xa0"))}}]),t}(a.Component),W=function(e){function t(e){var n;return Object(m.a)(this,t),(n=Object(h.a)(this,Object(f.a)(t).call(this,e)))._doFetchAppointments=function(e){return e.preventDefault(),n._fetchAppointments()},n._handlePrev=function(){var e=Object(u.a)(p.a.mark(function e(t){return p.a.wrap(function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,n.props.dispatchPrevPage(t);case 2:return e.next=4,n._fetchAppointments();case 4:case"end":return e.stop()}},e,this)}));return function(t){return e.apply(this,arguments)}}(),n._handleNext=function(){var e=Object(u.a)(p.a.mark(function e(t){return p.a.wrap(function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,n.props.dispatchNextPage(t);case 2:return e.next=4,n._fetchAppointments();case 4:case"end":return e.stop()}},e,this)}));return function(t){return e.apply(this,arguments)}}(),n.state={doctor:{},appointments:void 0,medical_institutions:void 0},n}return Object(b.a)(t,e),Object(d.a)(t,[{key:"componentDidMount",value:function(){var e=Object(u.a)(p.a.mark(function e(){var t,n=this;return p.a.wrap(function(e){for(;;)switch(e.prev=e.next){case 0:return t="".concat(w.baseURL,"/doctor/api/v1/public/profile/detail?id=").concat(this.props.state.doctor_id,"&fmt=sparse"),e.next=3,y.a.get(t).then(function(e){n.setState({doctor:e.data})}).catch(function(e){n.setState({doctor:void 0})});case 3:return e.next=5,this._fetchMedicalInstitutions();case 5:return e.next=7,this._fetchAppointments();case 7:case"end":return e.stop()}},e,this)}));return function(){return e.apply(this,arguments)}}()},{key:"_fetchMedicalInstitutions",value:function(){var e=Object(u.a)(p.a.mark(function e(){var t,n=this;return p.a.wrap(function(e){for(;;)switch(e.prev=e.next){case 0:return t="".concat(w.baseURL,"/doctor/api/v1/public/medical_institutions/connected/list?id=").concat(this.props.state.doctor_id),e.next=3,y.a.get(t).then(function(e){n.setState({medical_institutions:e.data})}).catch(function(e){n.setState({medical_institutions:void 0})});case 3:case"end":return e.stop()}},e,this)}));return function(){return e.apply(this,arguments)}}()},{key:"_fetchAppointments",value:function(){var e=Object(u.a)(p.a.mark(function e(){var t,n,a=this;return p.a.wrap(function(e){for(;;)switch(e.prev=e.next){case 0:return t=Y(this.props.state),n="".concat(w.baseURL,"/doctor/api/v1/private/appointment/list").concat(t),this.setState({appointments:void 0}),e.next=5,y.a.get(n).then(function(e){a.setState({appointments:e.data})}).catch(function(e){a.setState({appointments:[]})});case 5:case"end":return e.stop()}},e,this)}));return function(){return e.apply(this,arguments)}}()},{key:"render",value:function(){var e=this,t=[];return this.props.state.page>1?(t.push(r.a.createElement("a",{key:"0",href:"#!",onClick:function(){return e._handlePrev(e.props.state.page-1)}},"\xab Prev ",this.props.state.grab)),t.push(r.a.createElement("span",{key:"1"}," | Page: ",this.props.state.page," | ")),t.push(r.a.createElement("a",{key:"2",href:"#!",onClick:function(){return e._handleNext(e.props.state.page+1)}},"Next ",this.props.state.grab," \xbb"))):(t.push(r.a.createElement("span",{key:"1"}," Page: ",this.props.state.page," | ")),t.push(r.a.createElement("a",{key:"2",href:"#!",onClick:function(){return e._handleNext(e.props.state.page+1)}},"Next ",this.props.state.grab," \xbb"))),this.state.doctor?r.a.createElement("div",{className:"container"},r.a.createElement("div",{id:"filter-controls",className:"xcollapse"},r.a.createElement("div",{className:"row"},r.a.createElement("div",{className:"col-sm-12 col-md-6"},r.a.createElement("label",null,"Medical Institution"),r.a.createElement("br",null),r.a.createElement(E,{medical_institutions:this.state.medical_institutions})),r.a.createElement("div",{className:"col-sm-6 col-md-3"},r.a.createElement("label",null,"Start Date"),r.a.createElement("br",null),r.a.createElement(j,null)),r.a.createElement("div",{className:"col-sm-6 col-md-3"},r.a.createElement("label",null,"End Date"),r.a.createElement("br",null),r.a.createElement(N,null))),r.a.createElement("div",{className:"row mt-2"},r.a.createElement("div",{className:"col-sm-4"},r.a.createElement("label",null,"Appointment Type"),r.a.createElement("br",null),r.a.createElement(D,null)),r.a.createElement("div",{className:"col-sm-4"},r.a.createElement("label",null,"Status"),r.a.createElement("br",null),r.a.createElement(U,null)),r.a.createElement("div",{className:"col-sm-4"},r.a.createElement("label",null,"Display"),r.a.createElement("br",null),r.a.createElement(F,null))),r.a.createElement("div",{className:"row mt-2"},r.a.createElement("div",{className:"col-sm-12"},r.a.createElement("label",null,"Patient Name"),r.a.createElement(T,null)))),r.a.createElement("div",{className:"btn-group btn-group-sm text-right my-2"},r.a.createElement("a",{className:"btn btn-secondary btn-sm","data-toggle":"collapse",href:"#filter-controls"},r.a.createElement("i",{className:"fas fa-filter"},"\xa0")," Toggle Filters"),r.a.createElement("button",{type:"button",className:"btn btn-sm btn-primary",onClick:this._doFetchAppointments},r.a.createElement("i",{className:"fas fa-play"},"\xa0")," Filter List")),r.a.createElement("hr",null),r.a.createElement("div",null,t),r.a.createElement(V,{appointments:this.state.appointments})):r.a.createElement("div",{className:"alert alert-danger"},"Invalid Doctor")}}]),t}(a.Component),Z=Object(s.b)(function(e){return{state:e}},function(e){return{dispatchNextPage:function(t){return e({type:"UPDATE_PARAM",value:t,name:"page",cast:"int"})},dispatchPrevPage:function(t){return e({type:"UPDATE_PARAM",value:t,name:"page",cast:"int"})}}})(W);Boolean("localhost"===window.location.hostname||"[::1]"===window.location.hostname||window.location.hostname.match(/^127(?:\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}$/));var q=n(20),Q=n(39),$=new Date,z={doctor_id:0,medical_institution:"",s:"",day_start:new Date($.getTime()-6048e5).toISOString().split("T")[0],day_end:$.toISOString().split("T")[0],appointment_status:"",appointment_type:"",page:1,grab:50},G=Object(i.b)(function(){var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:z,t=arguments.length>1?arguments[1]:void 0;if("INITIALIZE_PARAMS"===t.type)return t.payload;if("UPDATE_PARAM"===t.type){var n=t.value;if(t.cast)switch(t.cast){case"int":n=parseInt(n);break;case"float":n=parseFloat(n)}return Object(Q.a)({},e,Object(q.a)({},t.name,n))}},window.__REDUX_DEVTOOLS_EXTENSION__&&window.__REDUX_DEVTOOLS_EXTENSION__());G.dispatch({type:"INITIALIZE_PARAMS",payload:window.appContext}),o.a.render(r.a.createElement(s.a,{store:G},r.a.createElement(Z,null)),document.getElementById("root")),"serviceWorker"in navigator&&navigator.serviceWorker.ready.then(function(e){e.unregister()})}},[[40,2,1]]]);
//# sourceMappingURL=main.893a3573.chunk.js.map