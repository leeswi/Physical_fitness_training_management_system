%rebase base title = '训练管理系统'

<div class="page-body">
    <div class="row">
        <div class="col-lg-5 col-md-5 col-sm-12 col-xs-12">
             <form action="" method="post">
             <div class="form-group-x">
				  <select id="name" style="width:70%;" name="name">
                    <option value=''>请选择要查询的对象</option>
                    %for name in name:
                        <option value='{{name.get('id','')}}'>{{name.get('name','')}}</option>
                    %end
                  </select>
             <button type="submit" class="btn btn-primary">提交</button>
             </div>

             <div id='main' style='width:500px;height:400px;margin-left:20px'></div>
                <script src='../assets/js/echarts.min.js' charset="utf-8" type="text/javascript"></script>
                <script>
                    function rager(name){
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
                                                    name: "选中项",
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
        <div class="col-lg-7 col-md-7 col-sm-12 col-xs-12">
            <form action="" method="post">
             <div class="form-group-x">
				  <select id="date" style="width:70%;" name="date">
                    <option value=''>请选择测试成绩</option>
                    %for date in date:
                        <option value='{{date.get('date','')}}'>{{date.get('subject','')}}</option>
                    %end
                  </select>
             <button type="submit" class="btn btn-primary">提交</button>
             </div>
            <div id='main2' style='width:700px;height:400px'></div>
            <script>
                var dom = document.getElementById("main2");
                var myChart = echarts.init(dom);
                var app = {};
                option = null;
                var posList = [
                    'left', 'right', 'top', 'bottom',
                    'inside',
                    'insideTop', 'insideLeft', 'insideRight', 'insideBottom',
                    'insideTopLeft', 'insideTopRight', 'insideBottomLeft', 'insideBottomRight'
                ];

                app.configParameters = {
                    rotate: {
                        min: -90,
                        max: 90
                    },
                    align: {
                        options: {
                            left: 'left',
                            center: 'center',
                            right: 'right'
                        }
                    },
                    verticalAlign: {
                        options: {
                            top: 'top',
                            middle: 'middle',
                            bottom: 'bottom'
                        }
                    },
                    position: {
                        options: echarts.util.reduce(posList, function (map, pos) {
                            map[pos] = pos;
                            return map;
                        }, {})
                    },
                    distance: {
                        min: 0,
                        max: 100
                    }
                };

                app.config = {
                    rotate: 90,
                    align: 'left',
                    verticalAlign: 'middle',
                    position: 'insideBottom',
                    distance: 15,
                    onChange: function () {
                        var labelOption = {
                            normal: {
                                rotate: app.config.rotate,
                                align: app.config.align,
                                verticalAlign: app.config.verticalAlign,
                                position: app.config.position,
                                distance: app.config.distance
                            }
                        };
                        myChart.setOption({
                            series: [{
                                label: labelOption
                            }, {
                                label: labelOption
                            }, {
                                label: labelOption
                            }, {
                                label: labelOption
                            }]
                        });
                    }
                };


                var labelOption = {
                    normal: {
                        show: true,
                        position: app.config.position,
                        distance: app.config.distance,
                        align: app.config.align,
                        verticalAlign: app.config.verticalAlign,
                        rotate: app.config.rotate,
                        formatter: '{c}  {name|{a}}',
                        fontSize: 16,
                        rich: {
                            name: {
                                textBorderColor: '#fff'
                            }
                        }
                    }
                };
                option = {
                    color: ['#003366', '#006699', '#4cabce', '#e5323e'],
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            type: 'shadow'
                        }
                    },
                    legend: {
                        data: ['五公里', '400米障碍', '引体向上', '卷身上']
                    },
                    toolbox: {
                        show: true,
                        orient: 'vertical',
                        top: 'center',
                        x:650,
                        feature: {
                            mark: {show: true},
                            dataView: {show: true, readOnly: false},
                            magicType: {show: true, type: ['line', 'bar', 'stack', 'tiled']},
                            restore: {show: true},
                            saveAsImage: {show: true}
                        }
                    },
                    calculable: true,
                    xAxis: [
                        {
                            type: 'category',
                            axisTick: {show: false},
                            data: ['优秀', '良好', '及格', '不及格']
                        }
                    ],
                    yAxis: [
                        {
                            type: 'value'
                        }
                    ],
                    series: [
                        {
                            name: '五公里',
                            type: 'bar',
                            barGap: 0,
                            label: labelOption,
                            data: [{{sum[0].get('w_youxiu',0)}},{{sum[0].get('w_lianghao',0)}},{{sum[0].get('w_jige',0)}},{{sum[0].get('w_bujige',0)}}]
                        },
                        {
                            name: '400米障碍',
                            type: 'bar',
                            label: labelOption,
                            data: [{{sum[0].get('z_youxiu',0)}},{{sum[0].get('z_lianghao',0)}},{{sum[0].get('z_jige',0)}},{{sum[0].get('z_bujige',0)}}]
                        },
                        {
                            name: '引体向上',
                            type: 'bar',
                            label: labelOption,
                            data: [{{sum[0].get('1_youxiu',0)}},{{sum[0].get('1_lianghao',0)}},{{sum[0].get('1_jige',0)}},{{sum[0].get('1_bujige',0)}}]
                        },
                        {
                            name: '卷身上',
                            type: 'bar',
                            label: labelOption,
                            data: [{{sum[0].get('2_youxiu',0)}},{{sum[0].get('2_lianghao',0)}},{{sum[0].get('2_jige',0)}},{{sum[0].get('2_bujige',0)}}]
                        }
                    ]
                };;
                if (option && typeof option === "object") {
                    myChart.setOption(option, true);
                }
            </script>
        </div>
    </div>
</div>
