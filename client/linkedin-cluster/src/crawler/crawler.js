import React, {Component} from 'react'
import axios from 'axios'
import {Button, message, Card, Table, Spin} from 'antd';

export default class Crawler extends Component {

    state = {
        userList: [],
        isStart: false,
        statusMsg: '',
        timer: null
    };

    componentWillMount = ()=> {
        axios.get('/api/crawler/status').then(res=> {
            const {status, data} = res.data;
            if (status === 0 && data.runningFlag === true) {
                this.setState({isStart: true});
                this.statusTimer();
            } else if(status === 1) {
                message.error('error happens when check status');
            }
        });

    };

    componentWillUnmount = ()=> {
        if (this.state.timer != null) {
            clearInterval(this.state.timer);
        }
    };

    onStart = ()=> {
        this.setState({userList: []});
        axios.get('/api/crawler/start').then(res=> {
            if (res.data.status === 0) {
                message.success('start crawler successfully');
                this.setState({isStart: true});
                this.statusTimer();
            } else {
                message.error('error happens when start');
            }
        })
    };

    onStop = ()=> {
        axios.get('/api/crawler/stop').then(res=> {
            if (res.data.status === 0) {
                message.success('stop crawler successfully');
                this.setState({isStart: false, statusMsg: ''});
                clearInterval(this.state.timer);
            } else {
                message.error('error happens when stop');
            }
        })
    };

    statusTimer = ()=> {
        const fetchStatus = ()=> {
            axios.get('/api/crawler/status').then(res=> {
                const {status, data} = res.data;
                if (status === 0 && data.runningFlag) {
                    //crawler is running
                    if (data.userList.length < 1) {
                        this.setState({statusMsg: 'Crawler is fetching profile url from google...'})
                    }
                    else {
                        this.setState({
                            statusMsg: 'Crawler is fetching linkedin profile..., totoal number: ' + data.userList.length,
                            userList: data.userList
                        })

                    }
                } else if (status === 0 && !data.runningFlag) {
                    //crawler is finished
                    this.setState({isStart: false, statusMsg: ''});
                    if (this.state.timer) {
                        clearInterval(this.state.timer);
                    }
                    message.success('crawler finished successfully');
                } else {
                    message.error('error happens when check status');
                }
            }).catch(error => {
                console.log(error.response);
                this.setState({isStart: false, statusMsg: ''});
                if (this.state.timer) {
                    clearInterval(this.state.timer);
                }
                message.error('error happens when check status');
            });
        };
        fetchStatus();
        const timer = setInterval(fetchStatus, 2000);
        this.setState({timer: timer});
    };

    fetchData = filename => {
        axios.get('api/userinfo/' + filename).then(res=> {
            const {status, data} = res.data;
            if (status === 0 && data) {
                this.setState({userList: data});
            }
        });
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
                    if (x == '500+') {
                        x = x.substring(0, x.length - 1)
                    }
                    if (y == '500+') {
                        y = y.substring(0, y.length - 1)
                    }
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
            <Card style={{margin: 20}}>
                <h4>For demo purpose, Crawl up to 100 profiles with key words 'developer' or 'designer'</h4>
                <h4>Only store the latest data, will clean the old data every time</h4>
            </Card>
            {!this.state.isStart &&
            <Button type='primary' onClick={this.onStart} style={{margin: 20}}>Start crawler</Button>}
            {this.state.isStart &&
            <Button type='danger' onClick={this.onStop} style={{margin: 20}} >Stop crawler</Button>}
            {this.state.statusMsg && <Card style={{width: 500, marginLeft: 20}}>
                <p style={{fontSize: 19, fontWeight: 600, display:'inline-block',marginRight:10}}>Monitor crawler status (updated every 2s)</p>
                <Spin/>
                <p style={{fontSize: 15}}>{this.state.statusMsg}</p>
            </Card>}
            <div style={{margin: 20}}>
                <Table
                    dataSource={dataSource}
                    columns={columns}
                    pagination={{pageSize: 10, total: dataSource.length}}
                    size="small"
                />
            </div>
        </div>)
    }

}


