import React, {Component} from 'react'
import axios from 'axios'
import {Button, message, Table} from 'antd';
import {G2, Chart, Geom, Axis, Tooltip, Coord, Label, Legend, View, Guide, Shape, Facet, Util} from "bizcharts";
export default class ClusterOne extends Component {

    state = {
        userList: [],
        points: []
    };

    componentWillMount = ()=> {
       this.fetchdata('userinfo_demo.csv')
    };

    fetchdata = fileName =>{
        axios.get('/api/userinfo/' + fileName).then(res=> {
            const {status, data} = res.data;
            if (status === 0 && data) {
                this.setState({userList: data});
            }
        });
        axios.get('/api/kmeans/0/' + fileName).then(res=> {
            const {status, data} = res.data;
            if (status === 0 && data) {
                this.setState({points: data});
            }else{
                this.setState({points: []});
                message.error(data);
            }
        })
    };

    render() {
        const dataSource = this.state.userList.map((elm, _index) => {
            return {
                key: _index,
                name: elm[0],
                level: elm[1],
                job: elm[2],
                location: elm[3],
                connection: elm[4],
                company: elm[5],
                college: elm[6],
                url: elm[7]
            }
        });
        const columns = [
            {
                title: 'index',
                dataIndex: 'key',
                key: 'key',
            },
            {
                title: 'name',
                dataIndex: 'name',
                key: 'name',
            },
            {
                title: 'level',
                dataIndex: 'level',
                key: 'level',
                sorter: (a, b) => a.level.charAt(0) - b.level.charAt(0)
            },
            {
                title: 'job',
                dataIndex: 'job',
                key: 'job',
            },
            {
                title: 'location',
                dataIndex: 'location',
                key: 'location',
            },
            {
                title: 'connection',
                dataIndex: 'connection',
                key: 'connection',
                sorter: (a, b) => {
                    let x = a.connection.split(' ')[0];
                    let y = b.connection.split(' ')[0];
                    if(x == '500+'){x = x.substring(0,x.length-1)}
                    if(y == '500+'){y = y.substring(0,y.length-1)}
                    return parseInt(x) - parseInt(y);
                }
            },
            {
                title: 'company',
                dataIndex: 'company',
                key: 'company',
            },
            {
                title: 'college',
                dataIndex: 'college',
                key: 'college',
            },
            {
                title: 'url',
                dataIndex: 'url',
                key: 'url',
            },
        ];
        return (
            <div>
                <Button onClick={()=>this.fetchdata('userinfo_demo.csv')} style={{margin: 20}}>Generate by Demo data</Button>
                <Button onClick={()=>this.fetchdata('userinfo.csv')} style={{margin: 20}}>Generate by Fetched data</Button>
                <div>
                    <Chart height={500} data={this.state.points} forceFit>
                        <Tooltip
                            showTitle={false}
                            crosshairs={{
                                type: "cross"
                            }}
                            itemTpl="<li data-index={index} style=&quot;margin-bottom:4px;&quot;><span style=&quot;background-color:{color};&quot; class=&quot;g2-tooltip-marker&quot;></span>{name}<br/>{value}</li>"
                        />
                        <Axis name="job" visible={true} title={true}/>
                        <Axis name="connection" visible={true} title={true}/>
                        <Legend />
                        <Geom
                            type="point"
                            position="job*connection"
                            color="group"
                            opacity={1}
                            shape="circle"
                            size={4}
                        />
                    </Chart>
                </div>
                <div style={{margin: 20}}>
                    <Table
                        dataSource={dataSource}
                        columns={columns}
                        pagination={{pageSize: 5, total: dataSource.length}}
                        size="small"
                    />
                </div>
            </div>
        )
    }

}


