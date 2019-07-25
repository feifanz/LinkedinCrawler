import React, {Component} from 'react'
import axios from 'axios'
import {Button, message, Card, Table} from 'antd';

export default class ClusterWne extends Component {

    state = {
        userGroup: [],
        topTerms: []
    };

    componentWillMount = ()=> {
        this.fetchdata('userinfo_demo.csv')
    };

    fetchdata = fileName => {
        axios.get('/api/kmeans/1/' + fileName).then(res=> {
            const {status, data} = res.data;
            if (status === 0 && data) {
                this.setState({userGroup: data.userGroup, topTerms: data.topTerms});
            }else{
                message.error(data);
                this.setState({userGroup: [], topTerms: []});
            }
        });

    };
    transData = dataSource => {
        return dataSource.map((elm, _index) => {
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
    };

    render() {
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
                <Card style={{margin: 20}}>
                    <h4>Use K-means to cluster data</h4>
                    <h4>use TF-IDF transfer the text of current job to numerical feature</h4>
                    <h4>For easy to draw diagram, cluster into 3 groups:</h4>
                    <h4>Also list top ten terms of each cluster</h4>
                </Card>
                <Button onClick={()=>this.fetchdata('userinfo_demo.csv')} style={{margin: 20}}>Generate by Demo
                    data</Button>
                <Button onClick={()=>this.fetchdata('userinfo.csv')} style={{margin: 20}}>Generate by Fetched
                    data</Button>
                <Card style={{margin: 20}}>
                    <p style={{fontSize: 19, fontWeight: 600}}>Top 10 Terms of each cluster</p>
                    {this.state.topTerms.map((elm, _index)=>(
                        <p key={_index}>{'Cluster'+_index+': '+elm.join(',')}</p>
                    ))}
                </Card>
                {this.state.userGroup.map((users, _index) => {
                    const dataSource = this.transData(users);
                    return (<div key={_index} style={{margin: 20}}>
                        <h3>Cluster{_index}</h3>
                        <Table
                            dataSource={dataSource}
                            columns={columns}
                            pagination={{pageSize: 5, total: dataSource.length}}
                            size="small"
                        />
                    </div>)
                })}
            </div>
        )
    }

}


