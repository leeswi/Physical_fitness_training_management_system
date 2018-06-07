%rebase base title='添加任务  日常训练管理系统',position='添加计划'
<div class="page-body">
    <div class="row">
        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">
            <div class="widget">
                <div class="widget-header bordered-bottom bordered-themesecondary">
                    <i class="widget-icon fa fa-tags themesecondary"></i>
                    <span class="widget-caption themesecondary">添加计划</span>
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
                  <form action="" method="post">
                    <div class="row">
                        <div class="input-group col-lg-4 col-md-4 col-md-offset-1 pull-left" style="padding:5px 0;margin-left:1.88%;">
                            <span class="input-group-addon">计划名</span>
                            <input type="text"  class="form-control" id="" name="subject" aria-describedby="inputGroupSuccess4Status" value="{{task_data[0].get('subject','')}}">
                        </div>
                        <div class="input-group col-lg-4 col-md-4 col-md-offset-1 pull-left" style="padding:5px 0;">
                            <span class="input-group-addon">负责人</span>
                            <select class="form-control" name="userid" id="user">
                                <option value="-1">-- 请选择执行责任人 --</option>
                                <option value="" disabled>------ 指定员工 ------</option>
                                %for user in user_data:
                                    <option value="{{user['id']}}">@{{user['name']}}</option>
                                %end
                            </select>
                        </div>
                    </div>

                    <div class="row">
                        <div class="input-group col-lg-4 col-md-4 col-md-offset-1 pull-left" style="padding:5px 0;margin-left:1.88%;">
                            <span class="input-group-addon">开始时间</span>
                            <input class="form-control date-picker" value="{{task_data[0].get('startdate','')}}" name="startdate" id="id-date-picker-1" type="text" data-date-format="yyyy-mm-dd" placeholder="请选择开始的开始日期">
                        </div>
                        <div class="input-group col-lg-4 col-md-4 col-md-offset-1 pull-left" style="padding:5px 0;">
                            <span class="input-group-addon">结束时间</span>
                            <input class="form-control date-picker" value="{{task_data[0].get('enddate','')}}" name="enddate" id="id-date-picker-2" type="text" data-date-format="yyyy-mm-dd" placeholder="请选择结束的结束日期">
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="submit" style="float:left" class="btn btn-primary">提交</button>
                    </div>
                </div>
              </form>
            </div>
        </div>
    </div>
</div>
<script src="/assets/js/datetime/bootstrap-datepicker.js"></script>
<script charset="utf-8" src="/assets/kindeditor/kindeditor.js"></script>
<script charset="utf-8" src="/assets/kindeditor/lang/zh_CN.js"></script>
<script>
    $('.date-picker').datepicker();     //时间插件
    KindEditor.ready(function(K) {
            window.editor = K.create('#editor_id');
    });
    $(function(){
        var userid = {{task_data[0].get('userid','-1')}}
        $('#user').val(userid);
    })
</script>
