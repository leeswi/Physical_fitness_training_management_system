%rebase base title='项目管理  日常训练管理系统',position='项目管理'
<div class="page-body">
    <div class="row">
        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">
            <div class="widget">
                <div class="widget-header bordered-bottom bordered-themesecondary">
                    <i class="widget-icon fa fa-tags themesecondary"></i>
                    <span class="widget-caption themesecondary">项目列表</span>
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
                <div style="padding:-10px 0px;" class="widget-body no-padding">
                    <div class="tickets-container">
                        <div class="table-toolbar" style="float:left">
                            <a id="adduser" href="/additem" class="btn btn-primary ">
                                <i class="btn-label fa fa-plus"></i>添加项目
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
    var editId;        //定义全局操作数据变量
	var isEdit;
    $('#myLoadTable').bootstrapTable({
          method: 'post',
          url: '/api/getitem',
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
              sortable: false,
          },{

              field: 'name',
              title: '项目名',
              align: 'center',
              valign: 'middle',
              sortable: false,
              formatter:url_link
          },{
              field: 'userid',
              title: '创建人',
              align: 'center',
              valign: 'middle',
              sortable: false
          },{
              field: 'itype',
              title: '项目类型',
              align: 'center',
			  valign: 'middle',
              sortable: false
          },{
              field: 'adddate',
              title: '创建时间',
              align: 'center',
              valign: 'middle',
              sortable: false
          },{
              field: 'startdate',
              title: '开始时间',
              align: 'center',
              valign: 'middle',
              sortable: false
          },{
              field: 'enddate',
              title: '结束时间',
              align: 'center',
              valign: 'middle',
              sortable: false
          },{
              field: 'status',
              title: '项目状态',
              align: 'center',
              valign: 'middle',
              sortable: false
          },{
              field: '',
              title: '操作',
              align: 'center',
              valign: 'middle',
              width:220,
              formatter:getinfo

          }]
      });

    //定义列操作
//    function getinfo(value,row,index){
//        eval('rowobj='+JSON.stringify(row))
//        return [
//            '<a href="/infoitem/'+rowobj['id']+'" class="btn-sm btn-success">',
//                '<i class="fa fa-arrow-circle-right"> 详情</i>',
//             '</a>',' ',
//            '<a href="/edititem/'+rowobj['id']+'" class="btn-sm btn-info">',
//                '<i class="fa fa-edit"> 编辑</i>',
//             '</a>',' ',
//            '<a href="/delitem/'+rowobj['id']+'" class="btn-sm btn-danger">',
//                '<i class="fa fa-times"> 删除</i>',
//             '</a>'
//        ].join('');
//    }
//
    //定义列操作
    function getinfo(value,row,index){
        eval('rowobj='+JSON.stringify(row));
        //定义编辑按钮样式，只有管理员或自己编辑的任务才有权编辑
        if({{session.get('access',None)}} == '1' || "{{session.get('name',None)}}" == rowobj['userid']){
            var style_edit = '<a href="/edititem/'+rowobj['id']+'" class="btn-sm btn-info" >';
        }else{
            var style_edit = '<a class="btn-sm btn-info" disabled>';
        }
        //定义删除按钮样式，只有管理员或自己编辑的任务才有权删除
        if({{session.get('access',None)}} == '1' || "{{session.get('name',None)}}" == rowobj['userid']){
            var style_del = '&nbsp;<a href="/delitem/'+rowobj['id']+'" class="btn-sm btn-danger">';
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


    //任务名的URL链接
    function url_link(value,row,index){
        eval('rowobj='+JSON.stringify(row))
        return [
            '<a href="/infoitem/'+rowobj['id']+'" style="text-decoration:none">',
                rowobj['name'],
             '</a>'
        ].join('');
    }


    /**
    *删除按钮操作
    */
    $('#deluser').popover({
                html: true,
                container: 'body',
                content : "<h3 class='btn btn-danger'>请选择要删除的记录</h3>",
                animation: false,
                placement : "top"
        }).on('click',function(){
            var res = $("#myLoadTable").bootstrapTable('getSelections');
            var str = '';
            if(res.length <= 0){
                $(this).popover("show");
                setTimeout("$('#deluser').popover('hide')",1000)
            }else{
                $(this).popover("hide");
                for(i in res){
                    str += res[i]['id']+',';
                }
                $.post('/deluser',{str:str},function(data){
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
</script>