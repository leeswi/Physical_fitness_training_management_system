%rebase base title='任务列表  日常训练管理系统',position='训练计划列表',managetopli="active open",adduser="active"

<div class="page-body">
    <div class="row">
        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">
            <div class="widget">
                <div class="widget-header bordered-bottom bordered-themesecondary">
                    <i class="widget-icon fa fa-tags themesecondary"></i>
                    <span class="widget-caption themesecondary">训练计划列表</span>
                    <div class="widget-buttons">
                        <a href="#" data-toggle="maximize">
                            <i class="fa fa-expand"></i>
                        </a>
                        <a href="#" data-toggle="collapse">
                            <i class="fa fa-minus"></i>
                        </a>
                        <a href="#" data-toggle="dispose">
                            <i class="fa fa-times"></i>
                        </a>
                    </div>

                </div><!--Widget Header-->
                <div class="widget-body  no-padding">
                    <div class="tickets-container">
						<div class="table-toolbar" style="float:left">
                            <a id="adduser" href="/addtask" class="btn btn-primary">
                                <i class="btn-label fa fa-plus"></i>发布计划
                            </a>
							<a id="adduser" href="/taskinfo" class="btn">
                                <i class="btn-label fa fa-home"></i>训练计划
                            </a>
							<a id="adduser" href="#" onclick = "getdata(0)" class="btn">
                                <i class="btn-label fa fa-times-circle" ></i>未开始
                            </a>
                            <a id="changeuser" href="#" onclick = "getdata(1)" class="btn">
                                <i class="btn-label fa fa-clock-o" ></i>进行中
                            </a>
                            <a id="deluser" href="#" class="btn" onclick = "getdata(2)">
                                <i class="btn-label fa fa-check-square-o" ></i>已完成
                            </a>
                        </div>
                       <table id="myLoadTable" class="table table-bordered table-hover"></table>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
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
              field: 'id',
              title: '编号',
              align: 'center',
              valign: 'middle',
              width:25,
              sortable: false
          },{
              field: 'planname',
              title: '计划名',
              align: 'center',
              valign: 'middle',
              sortable: false,
              formatter:getinfo1
          },{

              field: 'begin',
              title: '开始日期',
              align: 'center',
              valign: 'middle',
              sortable: false,
          },{
              field: 'end',
              title: '结束日期',
              align: 'center',
              valign: 'middle',
              sortable: false
          },{
              field: 'name',
              title: '负责人',
              align: 'center',
			  valign: 'middle',
              sortable: false,
          },{
              field: 'status',
              title: '状态',
              align: 'center',
              valign: 'middle',
              sortable: false,
              formatter:status
          },{
              field: '',
              title: '操作',
              align: 'center',
              valign: 'middle',
              width:200,
              formatter:getinfo  //？
          }]
      });

        //定义列操作
        function getinfo(value,row,index){
            eval('rowobj='+JSON.stringify(row));
            //定义编辑按钮样式，只有管理员或自己编辑的任务才有权编辑
            if({{session.get('access',None)}} == '1' || "{{session.get('name',None)}}" == rowobj['inputid']){
                var style_edit = '<a href="/edittask/'+rowobj['id']+'" class="btn-sm btn-info" >';
            }else{
                var style_edit = '<a class="btn-sm btn-info" disabled>';
            }
            //定义删除按钮样式，只有管理员或自己编辑的任务才有权删除
            if({{session.get('access',None)}} == '1' || "{{session.get('name',None)}}" == rowobj['inputid']){
                var style_del = '&nbsp;<a href="/deltask/'+rowobj['id']+'" class="btn-sm btn-danger">';
            }else{
                var style_del = '&nbsp;<a class="btn-sm btn-danger" disabled>';
            }
            return [
                style_edit,
                    '<i class="fa fa-edit"> 编辑</i>',
                '</a>',

                style_del,
                    '<i class="fa fa-times"> 删除</i>',
                '</a>'
            ].join('');
        }
        //
        function getinfo1(value,row,index){
            eval('rowobj='+JSON.stringify(row));
            console.log(JSON.stringify(row));
            return [
                '<a href="/infotask/'+rowobj['id']+'" style="text-decoration:none">',
                    rowobj['planname'],
                 '</a>'
            ].join('');
        }


        function status(value,row,index){
            eval('var rowobj='+JSON.stringify(row))
            var statusstr = '';
            if(rowobj['status'] == '0'){
                statusstr = '<span class="label label-danger">未开始</span>'
            }else if(rowobj['status'] == '1'){
                statusstr = '<span class="label label-success">进行中</span>'
            }else if(rowobj['status'] == '2'){
                statusstr = '<span class="label label-default">已完成</span>'
            }
            return [
                statusstr
            ].join('');
        }

        function priority(value,row,index){
			eval('var rowobj='+JSON.stringify(row))
			var prioritystr = '';
			if(rowobj['level'] == '1'){
				statusstr = '<span class="badge badge-info">1</span>'
			}else if(rowobj['level'] == '2'){
				statusstr = '<span class="badge badge-success">2</span>'
			}else if(rowobj['level'] == '3'){
				statusstr = '<span class="badge badge-warning">3</span>'
			}else if(rowobj['level'] == '4'){
				statusstr = '<span class="badge badge-danger">4</span>'
			}
			return [
				statusstr
			].join('');
        }
})
function getdata(param){
    $("#myLoadTable").bootstrapTable('refresh',{url: '/api/gettask?witchbtn='+param});
}

</script>
