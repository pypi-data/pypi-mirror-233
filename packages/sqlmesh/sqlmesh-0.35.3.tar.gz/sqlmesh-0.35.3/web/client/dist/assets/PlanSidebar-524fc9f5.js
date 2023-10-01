import{r as p,D as Te,ad as Oe,I as Be,y as Fe,w as re,B as Me,R as se,ae as Ie,af as ze,ag as $e,X as Re,ah as Ue,P as He,K as we,j as e,a6 as me,ai as Ee,a as Z,Z as L,aj as le,o as R,e as G,i as We,a1 as o,k as Ne,a4 as W,d as F,a0 as C,S as Ce,a3 as ae,a9 as oe,a2 as xe,c as $,ak as ke,u as Se,$ as Ve,al as Ge,ab as Le,n as je,a7 as Pe,am as Ke,E as _e,ac as qe}from"./index-22564d29.js";import{u as X,g as Ze,E as K,i as Xe,a as te,b as ge,c as f,P as Ye}from"./context-590d39df.js";import{M as Je,H as Qe,P as H}from"./PlanChangePreview-28eae11b.js";import{B as ee}from"./Banner-84b80980.js";import{T as pe}from"./TasksOverview-663e792f.js";import{v as I,M as ce,P as de}from"./disclosure-47be1803.js";import es from"./ReportErrors-e6cd2a81.js";import{I as q}from"./Input-e8c88e5c.js";import{s as ss}from"./popover-af5c7c25.js";import{T as ls,p as ns}from"./context-cc73b64e.js";import{S as as}from"./SplitPane-c87ab464.js";import"./ModelLineage-96ab515c.js";import"./PlusIcon-04528d91.js";import"./pluralize-d3f68cf8.js";import"./_commonjs-dynamic-modules-302442b1.js";let ye=p.createContext(null);ye.displayName="GroupContext";let ts=p.Fragment;function is(l){var s;let[n,a]=p.useState(null),[i,t]=Qe(),[c,m]=Ue(),w=p.useMemo(()=>({switch:n,setSwitch:a,labelledby:i,describedby:c}),[n,a,i,c]),h={},N=l;return se.createElement(m,{name:"Switch.Description"},se.createElement(t,{name:"Switch.Label",props:{htmlFor:(s=w.switch)==null?void 0:s.id,onClick(u){n&&(u.currentTarget.tagName==="LABEL"&&u.preventDefault(),n.click(),n.focus({preventScroll:!0}))}}},se.createElement(ye.Provider,{value:w},Re({ourProps:h,theirProps:N,defaultTag:ts,name:"Switch.Group"}))))}let rs="button";function os(l,s){let n=Be(),{id:a=`headlessui-switch-${n}`,checked:i,defaultChecked:t=!1,onChange:c,name:m,value:w,form:h,...N}=l,u=p.useContext(ye),g=p.useRef(null),E=Fe(g,s,u===null?null:u.setSwitch),[b,y]=ls(i,c,t),d=re(()=>y==null?void 0:y(!b)),P=re(v=>{if(He(v.currentTarget))return v.preventDefault();v.preventDefault(),d()}),j=re(v=>{v.key===we.Space?(v.preventDefault(),d()):v.key===we.Enter&&ns(v.currentTarget)}),S=re(v=>v.preventDefault()),T=p.useMemo(()=>({checked:b}),[b]),O={id:a,ref:E,role:"switch",type:ss(l,g),tabIndex:0,"aria-checked":b,"aria-labelledby":u==null?void 0:u.labelledby,"aria-describedby":u==null?void 0:u.describedby,onClick:P,onKeyUp:j,onKeyPress:S},U=Me();return p.useEffect(()=>{var v;let V=(v=g.current)==null?void 0:v.closest("form");V&&t!==void 0&&U.addEventListener(V,"reset",()=>{y(t)})},[g,y]),se.createElement(se.Fragment,null,m!=null&&b&&se.createElement(Ie,{features:ze.Hidden,...$e({as:"input",type:"checkbox",hidden:!0,readOnly:!0,form:h,checked:b,name:m,value:w})}),Re({ourProps:O,theirProps:N,slot:T,defaultTag:rs,name:"Switch"}))}let cs=Te(os),ds=is,he=Object.assign(cs,{Group:ds,Label:Je,Description:Oe});function us({show:l,children:s,afterLeave:n,onClose:a=()=>{}}){return e.jsx(me,{appear:!0,show:l,as:p.Fragment,afterLeave:n,children:e.jsxs(Ee,{as:"div",className:"relative z-[100] w-full h-full ",onClose:a,children:[e.jsx(me.Child,{as:p.Fragment,enter:"ease-out duration-300",enterFrom:"bg-overlay opacity-0",enterTo:"bg-overlay opacity-80",leave:"ease-in duration-200",leaveFrom:"bg-overlay opacity-80",leaveTo:"bg-overlay opacity-0",children:e.jsx("div",{className:"fixed inset-0"})}),e.jsx("div",{className:"w-full h-full fixed inset-0",children:e.jsx(me.Child,{as:p.Fragment,enter:"ease-out duration-300",enterFrom:"translate-x-[100%]",enterTo:"translate-x-0",leave:"ease-in duration-200",leaveFrom:"translate-x-0",leaveTo:"translate-x-[100%]",children:s})})]})})}function De({report:l}){return e.jsxs("div",{children:[e.jsxs("div",{className:"py-2",children:[e.jsxs("p",{children:["Total: ",l.total]}),e.jsxs("p",{children:["Succeeded: ",l.successful]}),e.jsxs("p",{children:["Failed: ",l.failures]}),e.jsxs("p",{children:["Errors: ",l.errors]}),e.jsxs("p",{children:["Dialect: ",l.dialect]})]}),e.jsx("ul",{children:l.details.map(s=>e.jsxs("li",{className:"flex mb-1",children:[e.jsx("span",{className:"inline-block mr-4",children:"—"}),e.jsxs("div",{className:"overflow-hidden",children:[e.jsx("span",{className:"inline-block mb-2",children:s.message}),e.jsx("code",{className:"inline-block max-h-[50vh] bg-theme py-2 px-4 rounded-lg w-full overflow-auto hover:scrollbar scrollbar--vertical scrollbar--horizontal",children:e.jsx("pre",{children:s.details})})]})]},s.message))})]})}function ms({setRefTasksOverview:l}){const{backfills:s,hasChanges:n,hasBackfills:a,activeBackfill:i,modified:t,added:c,removed:m,virtualUpdateDescription:w,skip_backfill:h,skip_tests:N,change_categorization:u,hasVirtualUpdate:g,testsReportErrors:E,testsReportMessages:b}=X(),y=Z(x=>x.environment),d=L(x=>x.state),P=L(x=>x.action),j=p.useMemo(()=>Array.from(u.values()).reduce((x,{category:k,change:_})=>{var D;return(D=_==null?void 0:_.indirect)==null||D.forEach(A=>{var z;x[A]==null&&(x[A]=[]),(z=x[A])==null||z.push(k.value!==1)}),k.value===3&&(x[_.model_name]=[!0]),x},{}),[u]),S=p.useCallback(x=>Object.entries(x).reduce((k,[_,D])=>{const A=j[_];return(A!=null?A.every(Boolean):!1)||(k[_]=D),k},{}),[j]),T=p.useCallback(x=>x.reduce((k,_)=>{const D=_.model_name,A=_.interval,z={completed:0,total:_.batches,interval:A,view_name:_.view_name},Q=j[D];return(Q!=null?Q.every(Boolean):!1)||(k[D]=z),k},{}),[j]),O=p.useMemo(()=>(i==null?void 0:i.tasks)!=null?S(i.tasks):T(s),[s,u,i]),U=d===C.Finished,v=[n,a,le(O)].every(R),V=g&&R(U)||R(v)&&a&&R(h)&&G(Object.keys(O)),Y=Ze({planAction:P,planState:d,hasBackfills:a,hasVirtualUpdate:g,hasNoChanges:v||We(Object.keys(O)),skip_backfill:h});return e.jsx("div",{className:"w-full h-full overflow-hidden overflow-y-auto p-4 hover:scrollbar scrollbar--vertical",children:e.jsx("ul",{className:"w-full",children:P===o.Run?e.jsx(M.StepOptions,{className:"w-full"}):e.jsxs(e.Fragment,{children:[e.jsx(fe,{headline:"Tests",description:"Report",disabled:y==null,children:P===o.Running?e.jsx(ie,{hasSpinner:!0,children:"Running Tests ..."}):Ne(E)&&Ne(b)?e.jsx(ie,{children:N?"Tests Skipped":"No Tests"}):e.jsxs(e.Fragment,{children:[E!=null&&e.jsx(ee,{variant:W.Danger,children:le(E)&&e.jsx(De,{report:E})}),b!=null&&e.jsx(ee,{variant:W.Success,children:le(b)&&e.jsx("div",{children:b.message})})]})}),e.jsx(fe,{headline:"Models",description:"Review Changes",disabled:y==null,children:n?e.jsxs(e.Fragment,{children:[(G(c)||G(m))&&e.jsxs("div",{className:"flex",children:[G(c)&&e.jsx(H,{className:"w-full m-2 max-h-[30vh]",headline:"Added Models",type:K.Add,children:e.jsx(H.Default,{type:K.Add,changes:c})}),G(m)&&e.jsx(H,{className:"w-full m-2 max-h-[30vh]",headline:"Removed Models",type:K.Remove,children:e.jsx(H.Default,{type:K.Remove,changes:m})})]}),Xe(t)&&e.jsxs(e.Fragment,{children:[G(t==null?void 0:t.direct)&&e.jsx(H,{className:"m-2 max-h-[30vh]",headline:"Modified Directly ",type:K.Direct,children:e.jsx(H.Direct,{changes:t.direct??[]})}),G(t.indirect)&&e.jsx(H,{className:"m-2 max-h-[30vh]",headline:"Modified Indirectly",type:K.Indirect,children:e.jsx(H.Indirect,{changes:t.indirect??[]})}),G(t==null?void 0:t.metadata)&&e.jsx(H,{className:"m-2 max-h-[30vh]",headline:"Modified Metadata",type:K.Metadata,children:e.jsx(H.Default,{type:K.Metadata,changes:(t==null?void 0:t.metadata)??[]})})]})]}):P===o.Running?e.jsx(ie,{hasSpinner:!0,children:"Checking Models..."}):e.jsx(ie,{children:"No Changes"})}),e.jsx(fe,{headline:"Backfill",description:"Progress",disabled:y==null,children:e.jsx(I,{defaultOpen:a,children:({open:x})=>e.jsxs(e.Fragment,{children:[e.jsx(ie,{hasSpinner:R(x)&&(P===o.Running||P===o.Applying),children:e.jsxs("div",{className:"flex justify-between items-center w-full",children:[e.jsx("div",{className:"flex items-center",children:e.jsx("h3",{className:F(d===C.Cancelled&&"text-prose",d===C.Failed&&"text-danger-700",d===C.Finished&&"text-success-700"),children:Y})}),V&&e.jsxs("div",{className:"flex items-center",children:[e.jsx("p",{className:"mr-2 text-sm",children:"Details"}),e.jsx(I.Button,{className:"flex items-center justify-between rounded-lg text-left text-sm",children:x?e.jsx(ce,{className:"h-6 w-6 text-primary-500"}):e.jsx(de,{className:"h-6 w-6 text-primary-500"})})]})]})}),e.jsxs(I.Panel,{className:"px-4 pb-2 text-sm",children:[a&&R(h)&&G(Object.keys(O))&&e.jsx(e.Fragment,{children:e.jsx(p.Suspense,{fallback:e.jsx(Ce,{className:"w-4 h-4 mr-2"}),children:e.jsx(pe,{tasks:O,setRefTasksOverview:l,children:({total:k,completed:_,models:D,completedBatches:A,totalBatches:z})=>e.jsxs(e.Fragment,{children:[e.jsx(pe.Summary,{environment:y.name,planState:d,headline:"Target Environment",completed:_,total:k,completedBatches:A,totalBatches:z,updateType:g?"Virtual":"Backfill",updatedAt:i==null?void 0:i.updated_at}),D!=null&&e.jsx(pe.Details,{models:D,changes:{modified:t,added:c,removed:m},showBatches:a,showVirtualUpdate:g,showProgress:!0})]})})})}),g&&e.jsx("div",{children:e.jsx("small",{className:"text-sm",children:w})})]})]})},Y)})]})})})}function ie({hasSpinner:l=!1,children:s}){return e.jsx("span",{className:"mt-1 mb-4 px-4 py-2 bg-primary-10 flex w-full rounded-lg",children:e.jsxs("span",{className:"flex items-center w-full",children:[l&&e.jsx(Ce,{className:"w-4 h-4 mr-2"}),s]})})}function fe({headline:l,description:s,children:n,disabled:a=!1}){return e.jsxs("li",{className:"mb-2 p-4",children:[e.jsx(ps,{className:"min-w-[25%] pr-12",headline:l,disabled:a,children:s}),!a&&n]})}function ps({disabled:l=!1,headline:s,children:n,className:a}){return e.jsxs("div",{className:F(l&&"opacity-40 cursor-not-allowed","mb-4 ",a),children:[s!=null&&e.jsx("h3",{className:"whitespace-nowrap font-bold text-lg",children:s}),n!=null&&e.jsx("small",{className:"whitespace-nowrap",children:n})]})}function hs(){const l=Z(n=>n.environment),{testsReportErrors:s}=X();return e.jsxs("div",{className:"flex flex-col py-2 w-full",children:[e.jsxs("div",{className:"flex justify-between",children:[e.jsxs("h4",{className:"text-xl pb-2 px-6",children:[e.jsx("span",{className:"font-bold",children:"Target Environment is"}),e.jsx("b",{className:"ml-2 px-2 py-1 font-sm rounded-md bg-primary-10 text-primary-500",children:l.name})]}),e.jsx("div",{className:"px-6",children:e.jsx(es,{})})]}),e.jsxs("div",{className:"w-full h-full overflow-auto hover:scrollbar scrollbar--vertical px-6 ",children:[l.isInitial&&l.isDefault&&e.jsx(ee,{variant:W.Warning,children:e.jsx(I,{defaultOpen:!0,children:({open:n})=>e.jsxs(e.Fragment,{children:[e.jsxs("div",{className:"flex items-center",children:[e.jsx(ee.Headline,{className:"w-full mr-2 text-sm mb-0",children:"Initializing Prod Environment"}),e.jsx(I.Button,{className:"flex items-center justify-between rounded-lg text-left text-sm",children:n?e.jsx(ce,{className:"h-6 w-6 text-warning-500"}):e.jsx(de,{className:"h-6 w-6 text-warning-500"})})]}),e.jsx(I.Panel,{className:"px-4 pb-2 text-sm mt-2",children:e.jsx(ee.Description,{children:"Prod will be completely backfilled in order to ensure there are no data gaps. After this is applied, it is recommended to validate further changes in a dev environment before deploying to production."})})]})})}),s!=null&&le(s)&&e.jsx(ee,{variant:W.Danger,children:e.jsx(I,{defaultOpen:!1,children:({open:n})=>e.jsxs(e.Fragment,{children:[e.jsxs("div",{className:"flex items-center",children:[e.jsx("p",{className:"w-full mr-2 text-sm",children:s==null?void 0:s.title}),e.jsx(I.Button,{className:"flex items-center justify-between rounded-lg text-left text-sm",children:n?e.jsx(ce,{className:"h-6 w-6 text-danger-500"}):e.jsx(de,{className:"h-6 w-6 text-danger-500"})})]}),e.jsx(I.Panel,{className:"px-4 pb-2 text-sm",children:e.jsx(De,{report:s})})]})})})]})]})}function fs(l=0){return p.useCallback(s=>{setTimeout(()=>{s==null||s.focus()},l)},[l])}function xs({planAction:l,disabled:s,run:n,apply:a,cancel:i,close:t,reset:c}){const{start:m,end:w,hasBackfills:h,skip_tests:N,auto_apply:u,skip_backfill:g,no_gaps:E,no_auto_categorization:b,forward_only:y,restate_models:d,include_unmodified:P,hasVirtualUpdate:j}=X(),S=Z(B=>B.environment),T=fs(),O=l===o.None,U=l===o.Run,v=l===o.Done,V=l===o.Cancelling,Y=l===o.Apply,x=l===o.Applying,k=l===o.Running,_=k||x||V;function D(B){B.stopPropagation(),t()}function A(B){B.stopPropagation(),c()}function z(B){B.stopPropagation(),i()}function Q(B){B.stopPropagation(),a()}function ne(B){B.stopPropagation(),n()}const ue=h&&R(g);return e.jsxs("div",{className:"flex justify-between px-4 py-2",children:[e.jsxs("div",{className:"flex w-full items-center",children:[(U||k)&&e.jsxs(ae,{disabled:k||s,onClick:ne,autoFocus:!0,ref:T,variant:W.Primary,children:[e.jsx("span",{children:te(l,[o.Running,o.Run])}),N&&e.jsx("span",{className:"inline-block ml-1",children:"And Skip Test"}),u&&e.jsx("span",{className:"inline-block ml-1",children:"And Auto Apply"})]}),(Y||x)&&e.jsx(ae,{onClick:Q,disabled:x||s,ref:T,variant:W.Primary,children:te(l,[o.Applying],ue?"Apply And Backfill":j?"Apply Virtual Update":"Apply")}),_&&e.jsx(ae,{onClick:z,variant:W.Danger,className:"justify-self-end",disabled:V||s,children:te(l,[o.Cancelling],"Cancel")}),(U||k||Y||x)&&e.jsxs("p",{className:"ml-2 text-xs max-w-sm",children:[e.jsx("span",{children:"Plan for"}),e.jsx("b",{className:"text-primary-500 font-bold mx-1",children:S.name}),e.jsx("span",{className:"inline-block mr-1",children:"environment"}),e.jsxs("span",{className:"inline-block mr-1",children:["from"," ",e.jsx("b",{children:R(oe(m))?m:"the begining of history"})]}),e.jsxs("span",{className:"inline-block mr-1",children:["till ",e.jsx("b",{children:R(oe(m))?w:"today"})]}),E&&e.jsxs("span",{className:"inline-block mr-1",children:["with ",e.jsx("b",{children:"No Gaps"})]}),g&&e.jsxs("span",{className:"inline-block mr-1",children:["without ",e.jsx("b",{children:"Backfills"})]}),y&&e.jsxs("span",{className:"inline-block mr-1",children:["consider as a ",e.jsx("b",{children:"Breaking Change"})]}),b&&e.jsxs("span",{className:"inline-block mr-1",children:["also set ",e.jsx("b",{children:"Change Category"})," manually"]}),R(oe(d))&&e.jsxs("span",{className:"inline-block mr-1",children:["and restate folowing models ",e.jsx("b",{children:d})]}),P&&e.jsx("span",{className:"inline-block mr-1",children:"with views for all models"})]})]}),e.jsxs("div",{className:"flex items-center",children:[(O||[_,U,s,S.isInitial&&S.isDefault,v].every(R))&&e.jsx(ae,{onClick:A,variant:W.Neutral,disabled:xe([o.Resetting,o.Running,o.Applying,o.Cancelling],l)||s,children:te(l,[o.Resetting],"Start Over")}),e.jsx(ae,{onClick:D,variant:v?W.Primary:W.Neutral,disabled:xe([o.Running,o.Resetting,o.Cancelling],l)||s,ref:v||x?T:void 0,children:te(l,[o.Done],"Close")})]})]})}function js({label:l,enabled:s,setEnabled:n,a11yTitle:a,size:i=$.md,disabled:t=!1,className:c}){return e.jsxs(he.Group,{as:"div",className:"flex items-center m-1",children:[e.jsxs(he,{checked:t?!1:s,onChange:n,className:F("flex relative border-secondary-30 rounded-full m-0","shrink-0 focus:outline-none ring-secondary-300 ring-opacity-60 ring-offset ring-offset-secondary-100 focus:border-secondary-500 focus-visible:ring-opacity-75","transition duration-200 ease-in-out",s?"bg-secondary-500":"bg-secondary-20",c,t?"opacity-50 cursor-not-allowed":"cursor-pointer",i===$.sm&&"h-[14px] w-6 focus:ring-1 border",i===$.md&&"h-5 w-10 focus:ring-2 border-2",i===$.lg&&"h-7 w-14 focus:ring-4 border-2"),disabled:t,children:[e.jsx("span",{className:"sr-only",children:a}),e.jsx("span",{"aria-hidden":"true",className:F("pointer-events-none inline-block transform rounded-full shadow-md transition duration-200 ease-in-out","bg-light",i===$.sm&&"h-3 w-3",i===$.md&&"h-4 w-4",i===$.lg&&"h-6 w-6",s&&i===$.sm&&"translate-x-[10px]",s&&i===$.md&&"translate-x-5",s&&i===$.lg&&"translate-x-7")})]}),l!=null&&e.jsx(he.Label,{className:F("text-xs font-light ml-1 text-neutral-600 dark:text-neutral-400"),children:l})]})}function J({label:l,info:s,enabled:n,disabled:a=!1,setEnabled:i,className:t}){return e.jsxs("div",{className:F("flex justify-between",t),children:[e.jsxs("label",{className:"block mb-1 px-3 text-sm font-bold",children:[l,e.jsx("small",{className:"block text-xs text-neutral-500",children:s})]}),e.jsx(js,{disabled:a,enabled:n,setEnabled:i,size:$.lg})]})}function gs({className:l}){const s=ge(),{skip_tests:n,no_gaps:a,skip_backfill:i,forward_only:t,auto_apply:c,no_auto_categorization:m,restate_models:w,isInitialPlanRun:h,create_from:N,include_unmodified:u}=X(),g=Z(y=>y.environment),E=Z(y=>y.environments),b=ke.getOnlySynchronized(Array.from(E));return e.jsx("li",{className:F("mt-6 mb-6",l),children:e.jsxs("form",{className:"w-full h-full",children:[e.jsxs("fieldset",{className:F("mb-10 mt-6"),children:[e.jsx("h2",{className:"whitespace-nowrap text-xl font-bold mb-1 px-4",children:"Set Dates"}),e.jsx("div",{className:"mt-3",children:e.jsx(M.BackfillDates,{})})]}),e.jsx("fieldset",{className:F("mb-4 mt-6"),children:e.jsx(I,{children:({open:y})=>e.jsxs(e.Fragment,{children:[e.jsxs(I.Button,{className:"flex items-center w-full justify-between rounded-lg text-left text-sm px-4 pt-3 pb-2 bg-neutral-10 hover:bg-theme-darker dark:hover:bg-theme-lighter",children:[e.jsx("h2",{className:"whitespace-nowrap text-xl font-bold mb-1",children:"Additional Options"}),y?e.jsx(ce,{className:"h-6 w-6 text-primary-500"}):e.jsx(de,{className:"h-6 w-6 text-primary-500"})]}),e.jsxs(I.Panel,{className:"px-4 pb-2 text-sm text-neutral-500",children:[e.jsx("div",{className:"mt-3",children:e.jsxs("div",{className:"flex flex-wrap md:flex-nowrap",children:[R(g.isDefault)&&e.jsx(q,{className:"w-full",label:"Create From Environment",info:"The environment to base the plan on rather than local files",disabled:b.length<2,children:({className:d,disabled:P})=>e.jsx(q.Selector,{className:F(d,"w-full"),list:ke.getOnlySynchronized(Array.from(E)).map(j=>({value:j.name,text:j.name})),onChange:j=>{s({type:f.PlanOptions,create_from:j})},value:N,disabled:P})}),e.jsx(q,{className:"w-full",label:"Restate Models",info:`Restate data for specified models and models
                        downstream from the one specified. For production
                        environment, all related model versions will have
                        their intervals wiped, but only the current
                        versions will be backfilled. For development
                        environment, only the current model versions will
                        be affected`,children:({className:d})=>e.jsx(q.Textfield,{className:F(d,"w-full"),placeholder:"project.model1, project.model2",disabled:h,value:w??"",onInput:P=>{P.stopPropagation(),s({type:f.PlanOptions,restate_models:P.target.value})}})})]})}),e.jsxs("div",{className:"flex flex-wrap md:flex-nowrap w-full mt-3",children:[e.jsxs("div",{className:"w-full md:mr-2",children:[e.jsx("div",{className:"block my-2",children:e.jsx(J,{label:"Skip Tests",info:`Skip tests prior to generating the plan if they
                  are defined`,enabled:!!n,setEnabled:d=>{s({type:f.PlanOptions,skip_tests:d})}})}),e.jsx("div",{className:"block my-2",children:e.jsx(J,{label:"No Gaps",info:`Ensure that new snapshots have no data gaps when
                  comparing to existing snapshots for matching
                  models in the target environment`,enabled:!!a,disabled:h,setEnabled:d=>{s({type:f.PlanOptions,no_gaps:d})}})}),e.jsx("div",{className:"block my-2",children:e.jsx(J,{label:"Skip Backfill",info:"Skip the backfill step",enabled:!!i,disabled:h,setEnabled:d=>{s({type:f.PlanOptions,skip_backfill:d})}})})]}),e.jsxs("div",{className:"w-full md:ml-2",children:[e.jsxs("div",{className:"block my-2",children:[e.jsx(J,{label:"Include Unmodified",info:"Indicates whether to create views for all models in the target development environment or only for modified ones",enabled:!!u,disabled:h,setEnabled:d=>{s({type:f.PlanOptions,include_unmodified:d})}}),e.jsx(J,{label:"Forward Only",info:"Create a plan for forward-only changes",enabled:!!t,disabled:h,setEnabled:d=>{s({type:f.PlanOptions,forward_only:d})}})]}),e.jsx("div",{className:"block my-2",children:e.jsx(J,{label:"Auto Apply",info:"Automatically apply the plan after it is generated",enabled:!!c,setEnabled:d=>{s({type:f.PlanOptions,auto_apply:d})}})}),e.jsx("div",{className:"block my-2",children:e.jsx(J,{label:"No Auto Categorization",info:"Set category manually",enabled:!!m,disabled:h,setEnabled:d=>{s({type:f.PlanOptions,no_auto_categorization:d})}})})]})]})]})]})})})]})})}function ys({disabled:l=!1}){const s=ge(),{start:n,end:a,isInitialPlanRun:i}=X();return e.jsxs("div",{className:"flex w-full flex-wrap md:flex-nowrap",children:[e.jsx(q,{className:"w-full md:w-[50%]",label:"Start Date (UTC)",info:"The start datetime of the interval",disabled:l||i,children:({disabled:t,className:c})=>e.jsx(q.Textfield,{className:F(c,"w-full"),disabled:t,placeholder:"2023-12-13",value:n,onInput:m=>{m.stopPropagation(),s({type:f.DateStart,start:m.target.value})}})}),e.jsx(q,{className:"w-full md:w-[50%]",label:"End Date (UTC)",info:"The end datetime of the interval",disabled:l||i,children:({disabled:t,className:c})=>e.jsx(q.Textfield,{className:F(c,"w-full"),disabled:t,placeholder:"2022-12-13",value:a,onInput:m=>{m.stopPropagation(),s({type:f.DateEnd,end:m.target.value})}})})]})}function bs({environment:l,isInitialPlanRun:s}){const{start:n,end:a,skip_tests:i,no_gaps:t,skip_backfill:c,forward_only:m,no_auto_categorization:w,restate_models:h,create_from:N,include_unmodified:u}=X(),g=p.useMemo(()=>{if(!l.isDefault)return{start:n,end:s&&oe(h)?void 0:a}},[l,n,a,s,h]);return{planOptions:p.useMemo(()=>l.isDefault||l.isInitial?{skip_tests:i,include_unmodified:!0}:{no_gaps:t,skip_backfill:c,forward_only:m,create_from:N,no_auto_categorization:w,skip_tests:i,restate_models:h,include_unmodified:u},[l,t,c,m,u,N,w,i,h]),planDates:g}}function vs({isInitialPlanRun:l}){const{start:s,end:n,skip_tests:a,no_gaps:i,skip_backfill:t,forward_only:c,include_unmodified:m,no_auto_categorization:w,restate_models:h,hasBackfills:N,create_from:u,change_categorization:g}=X(),E=p.useMemo(()=>{if(!(l||R(N)))return{start:s,end:n}},[N,s,n,l]),b=p.useMemo(()=>Array.from(g.values()).reduce((y,{category:d,change:P})=>(y[P.model_name]=d.value,y),{}),[g]);return{planDates:E,planOptions:{no_gaps:i,skip_backfill:t,forward_only:c,include_unmodified:m,create_from:u,no_auto_categorization:w,skip_tests:a,restate_models:h},categories:b}}function M({environment:l,isInitialPlanRun:s,initialStartDate:n,initialEndDate:a,disabled:i,onClose:t}){const c=ge(),{errors:m,removeError:w}=Se(),{auto_apply:h,hasChanges:N,hasBackfills:u,hasVirtualUpdate:g,testsReportErrors:E}=X(),b=L(r=>r.state),y=L(r=>r.action),d=L(r=>r.activePlan),P=L(r=>r.setActivePlan),j=L(r=>r.setAction),S=L(r=>r.setState),T=p.useRef(null),[O,U]=p.useState(!1),v=Ke(),V=bs({environment:l,isInitialPlanRun:s}),Y=vs({isInitialPlanRun:s}),{refetch:x,cancel:k}=Ve(l.name,V),{refetch:_,cancel:D}=Ge(l.name,Y),{refetch:A}=Le();p.useEffect(()=>{const r=v("tests",z);return l.isInitial&&l.isDefault&&ve(),c([{type:f.Dates,start:n,end:a}]),()=>{k(),r==null||r()}},[]),p.useEffect(()=>{c([{type:f.External,isInitialPlanRun:s}]),s&&c([{type:f.PlanOptions,skip_backfill:!1,forward_only:!1,no_auto_categorization:!1,no_gaps:!1,include_unmodified:!0}])},[s]),p.useEffect(()=>{R(O)&&l.isInitial||xe([C.Running,C.Applying,C.Cancelling],b)||(R(O)?j(o.Run):R(N||u)&&R(g)||b===C.Finished?j(o.Done):b===C.Failed?j(o.None):j(o.Apply))},[b,O,N,u,g]),p.useEffect(()=>{d!=null&&c({type:f.BackfillProgress,activeBackfill:d})},[d]),p.useEffect(()=>{m.size!==0&&(P(void 0),S(C.Failed))},[m]);function z(r){c([je(r.ok)?{type:f.TestsReportMessages,testsReportMessages:r}:{type:f.TestsReportErrors,testsReportErrors:r}])}function Q(){U(!1),c([{type:f.ResetBackfills},{type:f.ResetChanges},{type:f.Dates,start:n,end:a},{type:f.ResetPlanOptions}])}function ne(){j(o.Resetting),Q(),S(C.Init),j(o.Run)}function ue(){w(_e.RunPlan),w(_e.ApplyPlan),t()}function B(){c([{type:f.ResetTestsReport}]),S(C.Cancelling),j(o.Cancelling),(y===o.Applying?k:D)(),A().then(()=>{j(o.Run),S(C.Cancelled)}).catch(()=>{ne()})}function be(){j(o.Applying),S(C.Applying),c([{type:f.ResetTestsReport}]),_().then(({data:r})=>{(r==null?void 0:r.type)===qe.Virtual&&S(C.Finished)}).catch(console.log).finally(()=>{var r;(r=T==null?void 0:T.current)==null||r.scrollIntoView({behavior:"smooth",block:"start"})})}function ve(){c([{type:f.ResetTestsReport}]),j(o.Running),S(C.Running),x().then(({data:r})=>{c([{type:f.Backfills,backfills:r==null?void 0:r.backfills},{type:f.Changes,...r==null?void 0:r.changes},{type:f.Dates,start:r==null?void 0:r.start,end:r==null?void 0:r.end}]),U(!0),S(C.Init),h?be():j(o.Apply)})}const Ae=le(E);return e.jsxs("div",{className:"flex flex-col w-full h-full overflow-hidden pt-6",children:[Ae?e.jsxs(as,{sizes:le(E)?[50,50]:[30,70],direction:"vertical",snapOffset:0,className:"flex flex-col w-full h-full overflow-hidden",children:[e.jsx(M.Header,{}),e.jsx(M.Wizard,{setRefTasksOverview:T})]}):e.jsxs(e.Fragment,{children:[e.jsx(M.Header,{}),e.jsx(Pe,{}),e.jsx(M.Wizard,{setRefTasksOverview:T})]}),e.jsx(Pe,{}),e.jsx(M.Actions,{disabled:i,planAction:y,apply:be,run:ve,cancel:B,close:ue,reset:ne})]})}M.Actions=xs;M.Header=hs;M.Wizard=ms;M.StepOptions=gs;M.BackfillDates=ys;const Ms=p.memo(function(){const{isPlanOpen:s,setIsPlanOpen:n}=Se(),a=Z(u=>u.environment),i=Z(u=>u.initialStartDate),t=Z(u=>u.initialEndDate),c=L(u=>u.setAction),[m,w]=p.useState(!1);function h(){w(!0)}const N=je(s)&&R(m);return e.jsx(us,{show:N,afterLeave:()=>{c(o.None),w(!1),n(!1)},children:e.jsx(Ee.Panel,{className:"bg-theme border-8 border-r-0 border-secondary-10 dark:border-primary-10 absolute w-[90%] md:w-[75%] xl:w-[60%] h-full right-0 flex flex-col",children:e.jsx(Ye,{children:e.jsx(M,{environment:a,isInitialPlanRun:(a==null?void 0:a.isDefault)==null||je(a==null?void 0:a.isDefault),disabled:m,initialStartDate:i,initialEndDate:t,onClose:h})})})})});export{Ms as default};
