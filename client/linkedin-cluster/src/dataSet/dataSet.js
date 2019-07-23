import React, {Component} from 'react'
import axios from 'axios'
import { Button ,message,Card, Table} from 'antd';

export default class DataSet extends Component {

    state = {
        userList:[],

    };

    componentWillMount = ()=>{
        this.fetchData('userinfo.csv');
    };

    fetchData = filename =>{
        axios.get('api/userinfo/'+filename).then(res=>{
            const {status, data} = res.data;
            if(status === 0 && data){
                this.setState({userList:data});
            }
        });
    };

    render() {
        const dataSource = this.state.userList.map( (elm, _index) => {
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
        return (<div>
            <Button style={{margin:20}} onClick={() => this.fetchData('userinfo_demo.csv')}>Demo Data</Button>
            <Button style={{margin:20}} onClick={() => this.fetchData('userinfo.csv')}>Crawler Data</Button>
            <div style={{margin:20}}>
                <Table
                    dataSource={dataSource}
                    columns={columns}
                    pagination = {{pageSize: 10, total: dataSource.length}}
                    size="small"
                />
            </div>
        </div>)
    }

}


