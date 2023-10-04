"use strict";(self.webpackChunkatoti_jupyterlab=self.webpackChunkatoti_jupyterlab||[]).push([[7732],{27732:(e,t,a)=>{a.d(t,{FiltersBarDateRangePicker:()=>g});var r=a(52903),s=a(2242),i=a(62394),n=a(28879),l=a.n(n),c=a(74129),o=a(62144);const d=i.DatePicker.RangePicker,g=({filter:e,onFilterChanged:t})=>{const a=(0,o.Fg)(),{startDate:i,endDate:n}=e;return(0,r.BX)("div",{css:s.css`
        display: flex;
        align-items: center;
        border: 1px solid ${a.grayScale[5]};
        border-radius: 2px;
        max-height: 28px;
      `,children:[e.isExclusionFilter&&(0,r.tZ)(c.IconExclude,{style:{marginLeft:3,marginRight:5}}),(0,r.tZ)(d,{css:s.css`
          margin: 0 4px 0 0;
        `,value:[l()(i),l()(n)],onChange:a=>{const[r,s]=a,i={...e,startDate:r.toDate(),endDate:s.toDate()};t(i)},placement:"bottomLeft",bordered:!1,allowClear:!1})]})}}}]);