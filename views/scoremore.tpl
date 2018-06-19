%rebase base title = '训练管理系统'

<div class="page-body">
    <div class="row">
        <div class="col-lg-5 col-md-3 col-sm-12 col-xs-12">
             <form action="" method="post">
             <div class="form-group">
                  <label class="control-label" for="inputSuccess1">查询</label>
				  <select id="name" style="width:70%;" name="name">
                    <option value=''>请选择要查询的对象</option>
                    %for name in name:
                        <option value='{{name.get('id','')}}'>{{name.get('name','')}}</option>
                    %end
                  </select>
             <button type="submit" class="btn btn-primary">提交</button>
             </div>

             <div id='main' style='width:400px;height:400px;margin-left:20px'></div>
                <script src='../assets/js/echarts.min.js' charset="utf-8" type="text/javascript"></script>
                <script>
                    function rager(name){
                        console.log(name);
                    //基于准备好的DOM，初始化echarts实例
                        var myChart = echarts.init(document.getElementById('main'));
                          //指定图表的配置项和数据
                        var option = {
                                title: {
                                    text: '体能参数'
                                },
                                legend: {
                                    right:"5%",
                                    top:"1%",
                                    data: ['自己','及格','平均','选中项']
                                },
                                radar: [
                                    {
                                        indicator: [
                                            { text: '身高' , max:200},
                                            { text: '体重' , max:100},
                                            { text: '耐力' , max:100},
                                            { text: '速度' , max:100},
                                            { text: '力量' , max:100}
                                        ],
                                        center: ['50%', '50%'],
                                        radius: 120,
                                        startAngle: 90,
                                        splitNumber: 4,
                                        shape: 'circle',
                                        name: {
                                            formatter:'【{value}】',
                                            textStyle: {
                                                color:'#72ACD1'
                                            }
                                        },
                                        splitArea: {
                                            areaStyle: {
                                                color: ['rgba(114, 172, 209, 0.2)',
                                                'rgba(114, 172, 209, 0.4)', 'rgba(114, 172, 209, 0.6)',
                                                'rgba(114, 172, 209, 0.8)', 'rgba(114, 172, 209, 1)'],
                                                shadowColor: 'rgba(0, 0, 0, 0.3)',
                                                shadowBlur: 10
                                            }
                                        },
                                        axisLine: {
                                            lineStyle: {
                                                color: 'rgba(255, 255, 255, 0.5)'
                                            }
                                        },
                                        splitLine: {
                                            lineStyle: {
                                                color: 'rgba(255, 255, 255, 0.5)'
                                            }
                                        }
                                    },
                                ],
                                series: [
                                    {
                                        name: '雷达图',
                                        type: 'radar',
                                        itemStyle: {
                                            emphasis: {
                                                // color: 各异,
                                                lineStyle: {
                                                    width: 4
                                                }
                                            }
                                        },
                                        data: [
                                            {
                                                value: [{{result[0].get('height',0)}}, {{result[0].get('weight',0)}}, {{result[0].get('naili',0)}},{{result[0].get('sudu',0)}}, {{result[0].get('liliang',"0")}}],
                                                name: '自己',
                                                symbol: 'rect',
                                                symbolSize: 5,
                                                areaStyle: {
                                                    normal: {
                                                        color: 'rgba(255, 255, 255, 0.5)'
                                                    }
                                                }
                                            },
                                            {
                                                value: [170,60,14,17,39],
                                                name: '及格',
                                                areaStyle: {
                                                    normal: {
                                                        color: 'rgba(255, 255, 255, 0.5)'
                                                    }
                                                }
                                            },
                                            {
                                                value: [{{AVG_result[0].get('height',0)}}, {{AVG_result[0].get('weight',0)}}, {{AVG_result[0].get('naili',0)}},{{AVG_result[0].get('sudu',0)}}, {{AVG_result[0].get('liliang',0)}}],
                                                name: '平均',
                                                areaStyle: {
                                                    normal: {
                                                        color: 'rgba(255, 255, 255, 0.5)'
                                                    }
                                                }
                                            },
                                            %if(select):
                                                {
                                                    value: [{{select[0].get('height',0)}}, {{select[0].get('weight',0)}}, {{select[0].get('naili',0)}},{{select[0].get('sudu',0)}}, {{select[0].get('liliang',0)}}],
                                                    name: '选中项',
                                                    lineStyle: {
                                                        normal: {
                                                        type: 'dashed'
                                                        }
                                                    }
                                                }
                                            %end
                                        ]
                                    }
                                ]
                            }
                        //使用刚指定的配置项和数据显示图表
                        myChart.setOption(option);}
                rager();
                </script>
        </div>
        <div class="col-lg-3 col-md-3 col-sm-12 col-xs-12">
            右上位置（先占位）
        </div>
    </div>
</div>
