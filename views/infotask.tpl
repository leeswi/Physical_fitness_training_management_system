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
						<div class="" style="line-height:25px;margin-bottom:15px;"><b>【管理员:{{taskinfo[0].get('name','未知')}}】（时间：{{taskinfo[0].get('startdate','未知')}}至{{taskinfo[0].get('enddate','未知')}}）</b></div>
						<div style="margin-bottom:15px;">
							<span class="label label-info" style="font-size:16px;">内容</span>
						</div>
                        <div class="tickets-container">
                            <div class="table-toolbar" style="float:left">
                                    <a id="addtask" href="javascript:void(0);" class="btn  btn-primary ">
                                    <i class="btn-label fa fa-plus"></i>添加计划项目
                                </a>
                                <a id="changetask" href="javascript:void(0);" class="btn btn-warning shiny">
                                    <i class="btn-label fa fa-cog"></i>修改计划项目
                                </a>
                                <a id="deltask" href="javascript:void(0);" class="btn btn-darkorange">
                                    <i class="btn-label fa fa-times"></i>删除计划项目
                                </a>
                            </div>
                           <table id="myLoadTable" class="table table-bordered table-hover"></table>
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
                          <span class="widget-caption themeprimary">操作</span>
                      </div>
                  </div>
                </div>
           </div>
        </div>
    </div>
</div>
<div class="modal fade" id="myModal" tabindex="-1" role="dialog"  aria-labelledby="myModalLabel" aria-hidden="true">
    <div class="modal-dialog" >
      <div class="modal-content" id="contentDiv">
         <div class="widget-header bordered-bottom bordered-blue ">
           <i class="widget-icon fa fa-pencil themeprimary"></i>
           <span class="widget-caption themeprimary" id="modalTitle">添加计划项目</span>
        </div>

         <div class="modal-body">
            <div>
            <form id="modalForm">
                <div class="form-group">
                  <label class="control-label" for="inputSuccess1">日期：</label>
                  <input type="date" class="form-control" id="date" name="date" require>
                </div>
                <div class="form-group">
                  <label class="control-label" for="inputSuccess1">时间：</label>
                  <input type="time" class="form-control" id="begintime" name="begintime" require>
                </div>
                <div class="form-group">
                  <label class="control-label" for="inputSuccess1">时长：</label>
                  <input type="number" min='0' class="form-control" id="lasttime" name="lasttime" require>
                </div>
                <div class="form-group">
                  <label class="control-label" for="inputSuccess1">训练内容：</label>
                  <select id="content" style="width:100%;" name="content">
                      <option value=''>请选择训练内容</option>
                        %for name in content:
                            <option value='{{name.get('content','')}}'>{{name.get('content','')}}</option>
                        %end
                  </select>
                </div>
                <div class="form-group">
                  <label class="control-label" for="inputSuccess1">训练场地：</label>
                  <select id="place" style="width:100%;" name="place">
                      <option value=''>请选择训练场地</option>
                        %for name in place:
                            <option value='{{name.get('place','')}}'>{{name.get('place','')}}</option>
                        %end
                  </select>
                </div>
                <div class="form-group">
                  <label class="control-label" for="inputSuccess1">分组：</label>
                  <select id="teamid" style="width:100%;" name="teamid">
                    <option value=''>请选择组训单位</option>
                    %for name in teamid:
                        <option value='{{name.get('name','')}}'>{{name.get('name','')}}</option>
                    %end
                 </select>
                </div>
                <br></br>
                <input type="hidden" id="hidInput" value="">
                <button type="button" id="subBtn" class="btn btn-primary  btn-sm">提交</button>
                <button type="button" class="btn btn-warning btn-sm" data-dismiss="modal">关闭</button>
             </form>
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
          url: '/api/gettaskinfo/'+{{taskinfo[0].get('id','未知')}},
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
          sortName: 'date',
          columns: [{
              field: 'bianhao',
              title: 'checkbox',
              checkbox: true,
          },{
              field: 'date',
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
              field: 'lasttime',
              title: '时长(mins)',
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
              formatter:levels
          },{
              field: 'name',
              title: '负责人',
              align: 'center',
              valign: 'middle',
              sortable: false
          },{
              field: 'SignIn',
              title: '签到',
              align: 'center',
              valign: 'middle',
              sortable: false,
              formatter:priority
          },{
              field: '',
              title: '操作',
              align: 'center',
              valign: 'middle',
              formatter:getinfo
          }]
      });

    //定义列操作
    function getinfo(value,row,index){
            eval('rowobj='+JSON.stringify(row))
			if(rowobj['SignIn'] == '0'){
				return [
					'<a href="/taskSignIn/'+rowobj['id']+'/'+rowobj['tid']+'" class="btn-sm btn-info">',
						'<i class="fa fa-bell-o">签到</i>',
					 '</a>',
				].join('');
			}else{
				return [
					'<i class="fa fa-bell">已签到</i>',
				].join('');
			}
        }

    function priority(value,row,index){
					eval('var rowobj='+JSON.stringify(row))
					if(rowobj['SignIn'] == '0'){
						statusstr = '<span class="badge badge-danger">×</span>'
					}else if(rowobj['SignIn'] == '1'){
						statusstr = '<span class="badge badge-success">√</span>'
					}
					return [
						statusstr
					].join('');
				}

	function levels(value,row,index){
    			eval('var rowobj='+JSON.stringify(row))
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

	var editId;        //定义全局操作数据变量
    var editTid;
	var isEdit;
	/**
    *添加弹出框
    */
	$('#addtask').click(function(){
        $('#modalTitle').html('添加计划项目');
        $('#hidInput').val('0');
        $('#myModal').modal('show');
        $('#modalForm')[0].reset();
        isEdit = 0;
        editId = {{taskinfo[0].get('id','未知')}};
    });
    /**
    *修改弹出框
    */
    $('#changetask').popover({
    	    html: true,
    	    container: 'body',
    	    content : "<h3 class='btn btn-danger'>请选择一条进行操作</h3>",
    	    animation: false,
    	    placement : "top"
    }).on('click',function(){
    		var result = $("#myLoadTable").bootstrapTable('getSelections');
    		if(result.length <= 0){
    			$(this).popover("show");
    			setTimeout("$('#changetask').popover('hide')",1000)
    		}
    		if(result.length > 1){
    			$(this).popover("show");
    			setTimeout("$('#changetask').popover('hide')",1000)
    		}
    		if(result.length == 1){
                $('#changetask').popover('hide');
                $('#date').val(result[0]['date']);
                $('#begintime').val(result[0]['begintime']);
                $('#lasttime').val(result[0]['lasttime']);
                $('#content').val(result[0]['content']);
                $('#place').val(result[0]['place']);
                $('#teamid').val(result[0]['teamid']);
                $('#modalTitle').html('修改项目计划');     //头部修改
                $('#hidInput').val('1');            //修改标志
                $('#myModal').modal('show');
                editId = result[0]['id'];
                editTid = result[0]['tid'];
				isEdit = 1;
    		}
        });
    /**
    *提交按钮操作
    */
    $("#subBtn").click(function(){
           var date = $('#date').val();
           var begintime = $('#begintime').val();
           var lasttime = $('#lasttime').val();
           var content = $('#content').val();
           var place = $('#place').val();
           var teamid = $('#teamid').val();
           var postUrl;
           console.log(date);
           if(isEdit==1){
                postUrl = "/changetaskinfo/"+editId+"/"+editTid;           //修改路径
                console.log(postUrl);
           }else{
                postUrl = "/addtaskinfo/"+editId;          //添加路径
                console.log(postUrl);
           }
           $.post(postUrl,{date:date,begintime:begintime,lasttime:lasttime,content:content,place:place,teamid:teamid},function(data){
                  if(data==0){
                    $('#myModal').modal('hide');
                    $('#myLoadTable').bootstrapTable('refresh');
                    message.message_show(200,200,'成功','操作成功');
                  }else if(data==-1){
                      message.message_show(200,200,'失败','操作失败');
                  }else{
                        console.log(data);return false;
                }
            },'html');
       });

        /**
        *删除按钮操作
        */
    $('#deltask').popover({
                html: true,
                container: 'body',
                content : "<h3 class='btn btn-danger'>请选择要删除的记录</h3>",
                animation: false,
                placement : "top"
        }).on('click',function(){
            var res = $("#myLoadTable").bootstrapTable('getSelections');
            var str = '';
            var id = res[0]['id'];
            if(res.length <= 0){
                $(this).popover("show");
                setTimeout("$('#deltask').popover('hide')",1000)
            }else{
                $(this).popover("hide");
                for(i in res){
                    str += res[i]['tid']+',';
                }
                $.post('/deltaskinfo',{id:id,str:str},function(data){
                    if(data==0){
                        message.message_show(200,200,'删除成功',res.length+'条记录被删除');
                        $('#myLoadTable').bootstrapTable('refresh');
                    }else{
                        message.message_show(200,200,'失败','删除失败');
                    }
                },'html');

            }
        });

})
function getdata(param){
    console.log("2");
    $("#myLoadTable").bootstrapTable('refresh',{url: '/infotask?witchbtn='+param});

}
</script>
