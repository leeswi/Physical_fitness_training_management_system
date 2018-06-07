%rebase base title='任务详细  日常训练管理系统',position='任务详细'
<div class="page-body">
    <div class="row">
        <div class="col-lg-9 col-md-9 col-sm-12 col-xs-12">
            <div class="widget">
                <div class="widget-header bordered-bottom bordered-themesecondary" style="height:65px">
                    <i class="themesecondary" style="font-size:200%;line-height:65px;margin-left:10px;"></i>
                    <span class="widget-caption themesecondary" ><h3><b style="font-family:微软雅黑">【{{taskinfo[0].get('planname','未知')}}】 </b></h3></span>
                </div>
                <div class="widget-body  no-padding">
                    <div class="tickets-container">
						<div class="" style="line-height:25px;margin-bottom:15px;"><b>【管理员:{{taskinfo[0].get('name','未知')}}】</b>于{{taskinfo[0].get('inputdate','')}}发布<b>【负责人:{{taskinfo[0].get('name','未知')}}】</b></h4></div>
						<div style="margin-bottom:15px;">
							<span class="label label-info" style="font-size:16px;">内容</span>
						</div>
						<div>
						<table id="myLoadTable" class="table table-bordered table-hover"></table>
						</div>
                    </div>
                </div>
            </div>
        </div>
       <div class="col-lg-3 col-md-3 col-sm-12 col-xs-12">
           <div class="orders-container">
               <div class="row">
                  <div class="col-lg-12 col-sm-12 col-xs-12">
                      <div class="widget-header bordered-bottom bordered-blue ">
                          <i class="widget-icon fa fa-pencil themeprimary"></i>
                          <span class="widget-caption themeprimary">任务操作</span>
                      </div>
                  </div>
                </div>
           </div>
        </div>
    </div>
</div>

<script src="/assets/js/datetime/bootstrap-datepicker.js"></script>
<script type="text/javascript">
$(function(){
    /**
    *表格数据
    */
    $('#myLoadTable').bootstrapTable({
          method: 'post',
          url: '/api/gettask',
          contentType: "application/json",
          datatype: "json",
          cache: false,
          checkboxHeader: true,
          striped: true,
          pagination: true,
          pageSize: 15,
          pageList: [10,20,50],
          search: true,
          showColumns: true,
          showRefresh: true,
          minimumCountColumns: 2,
          clickToSelect: true,
          smartDisplay: true,
          //sidePagination : "server",
          sortOrder: 'asc',
          sortName: 'id',
          columns: [{
              field: 'dates',
              title: '日期',
              align: 'center',
              valign: 'middle',
              sortable: false
          },{

              field: 'begintime',
              title: '时间',
              align: 'center',
              valign: 'middle',
              sortable: false,
          },{
              field: 'content',
              title: '训练内容',
              align: 'center',
              valign: 'middle',
              sortable: false
          },{
              field: 'place',
              title: '训练场地',
              align: 'center',
              valign: 'middle',
              sortable: false
          },{
              field: 'teamid',
              title: '分组',
              align: 'center',
              valign: 'middle',
              sortable: false
          },{
              field: 'level',
              title: '强度',
              align: 'center',
			  valign: 'middle',
              sortable: false,
          },{
              field: 'status',
              title: '状态',
              align: 'center',
              valign: 'middle',
              sortable: false,
          },{
              field: 'name',
              title: '负责人',
              align: 'center',
              valign: 'middle',
              sortable: false
          },{
              field: '',
              title: '操作',
              align: 'center',
              valign: 'middle',
              width:200,

          }]
      });



})
function getdata(param){
    console.log("2");
    $("#myLoadTable").bootstrapTable('refresh',{url: '/infotask?witchbtn='+param});

}
</script>
