%rebase base title='成绩管理  日常训练管理系统',position='成绩管理',managetopli="active open",adduser="active"
<div class="page-body">
    <div class="row">
        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">
            <div class="widget">
                <div class="widget-header bordered-bottom bordered-themesecondary">
                    <i class="widget-icon fa fa-tags themesecondary"></i>
                    <span class="widget-caption themesecondary">成绩单管理</span>
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
                            <a id="addscorelist" href="javascript:void(0);" class="btn btn-primary">
                                <i class="btn-label fa fa-plus"></i>发布成绩单
                            </a>
                            <a id="changescore" href="javascript:void(0);" class="btn btn-warning shiny">
                                <i class="btn-label fa fa-cog"></i>修改成绩单
                            </a>
							<a id="adduser" href="/score" class="btn">
                                <i class="btn-label fa fa-home"></i>成绩单管理
                            </a>
                        </div>
                       <table id="myLoadTable" class="table table-bordered table-hover"></table>
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
           <span class="widget-caption themeprimary" id="modalTitle">添加成绩单</span>
        </div>

         <div class="modal-body">
            <div>
            <form id="modalForm">
                <div class="form-group">
                  <label class="control-label" for="inputSuccess1">成绩单名称：</label>
                  <input type="text" class="form-control" id="name" name="name" require>
                </div>
                <div class="form-group">
                  <label class="control-label" for="inputSuccess1">日期：</label>
                  <input type="date" class="form-control" id="date" name="date">
                 </select>
                </div>
                <div class="form-group">
                  <label class="control-label" for="inputSuccess1">负责人：</label>
				  <select id="chargeman" style="width:100%;" name="chargeman">
                    <option value=''>请选择负责人</option>
                    <option value='{{session.get('name',None)}}'>{{session.get('name',None)}}</option>
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
<script type="text/javascript">
$(function(){
    /**
    *表格数据
    */
    var editId;        //定义全局操作数据变量
	var isEdit;
	/**
    *添加弹出框
    */
	$('#addscorelist').click(function(){
        $('#modalTitle').html('添加成绩单');
        $('#hidInput').val('0');
        $('#myModal').modal('show');
        $('#modalForm')[0].reset();
        isEdit = 0;
    });
	/**
    *修改弹出框
    */
    $('#changescore').popover({
    	    html: true,
    	    container: 'body',
    	    content : "<h3 class='btn btn-danger'>请选择一条进行操作</h3>",
    	    animation: false,
    	    placement : "top"
    }).on('click',function(){
    		var result = $("#myLoadTable").bootstrapTable('getSelections');
    		if(result.length <= 0){
    			$(this).popover("show");
    			setTimeout("$('#changescore').popover('hide')",1000)
    		}
    		if(result.length > 1){
    			$(this).popover("show");
    			setTimeout("$('#changescore').popover('hide')",1000)
    		}
    		if(result.length == 1){
                $('#changescore').popover('hide');
                $('#name').val(result[0]['subject']);
                $('#date').val(result[0]['date']);
                $('#modalTitle').html('修改成绩单');     //头部修改
                $('#hidInput').val('1');            //修改标志
                $('#myModal').modal('show');
                editId = result[0]['id'];
				isEdit = 1;
    		}
        });
    $('#myLoadTable').bootstrapTable({
          method: 'post',
          url: '/api/getscorelist',
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
              field: 'bianhao',
              title: 'checkbox',
              checkbox: true,
          },{
              field: 'id',
              title: '编号',
              align: 'center',
              valign: 'middle',
              width:25,
              sortable: false
          },{
              field: 'subject',
              title: '成绩单',
              align: 'center',
              valign: 'middle',
              sortable: false,
              formatter:getinfo1
          },{

              field: 'date',
              title: '日期',
              align: 'center',
              valign: 'middle',
              sortable: false,
          },{
              field: 'inputid',
              title: '管理员',
              align: 'center',
              valign: 'middle',
              sortable: false
          },{
              field: '',
              title: '操作',
              align: 'center',
              valign: 'middle',
              width:200,
              formatter:getinfo  //？
          }]
      });

    /**
    *提交按钮操作
    */
    $("#subBtn").click(function(){
           var subject = $('#name').val();
           var date = $('#date').val();
           var chargeman = $('#chargeman').val();
           var postUrl;
           if(isEdit==1){
                postUrl = "/changescore/"+editId;           //修改路径
                console.log(postUrl);
           }else{
                postUrl = "/addscorelist";          //添加路径
                console.log(postUrl);
           }

           $.post(postUrl,{subject:subject,date:date,chargeman:chargeman},function(data){
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
                var style_del = '&nbsp;<a href="/delscore/'+rowobj['id']+'" class="btn-sm btn-danger">';
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
                '<a href="/infoscore/'+rowobj['date']+'" style="text-decoration:none">',
                    rowobj['subject'],
                 '</a>'
            ].join('');
        }

})
function getdata(param){
    $("#myLoadTable").bootstrapTable('refresh',{url: '/api/gettask?witchbtn='+param});
}

</script>
