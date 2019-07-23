import React, {Component} from 'react'
import './App.css';
import 'antd/dist/antd.css'
import {Menu, Icon} from 'antd';
import Crawler from './crawler/crawler'
import ClusterOne from './cluster/clusterOne'
import ClusterTwo from './cluster/clusterTwo'
import DataSet from './dataSet/dataSet';

export default class App extends Component {
    state = {
        current: 'dataSet',
    };

    handleClick = e => {
        console.log('click ', e);
        this.setState({
            current: e.key,
        });
    };

    render() {
        const {SubMenu} = Menu;
        return (
            <div>
                <Menu onClick={this.handleClick} selectedKeys={[this.state.current]} mode="horizontal">
                    <Menu.Item key="crawler">
                        <Icon type="mail"/>
                        crawler
                    </Menu.Item>
                    <SubMenu
                        title={
                            <span className="submenu-title-wrapper">
                              <Icon type="setting"/>
                                    cluster
                            </span>
                        }
                    >
                        <Menu.Item key="clusterOne">clusterOne</Menu.Item>
                        <Menu.Item key="clusterTwo">clusterTwo</Menu.Item>
                    </SubMenu>
                    <Menu.Item key="dataSet">
                        <Icon type="mail"/>
                        dataSet
                    </Menu.Item>

                </Menu>
                {this.state.current === 'crawler' && <Crawler/>}
                {this.state.current === 'clusterOne' && <ClusterOne/>}
                {this.state.current === 'clusterTwo' && <ClusterTwo/>}
                {this.state.current === 'dataSet'&&<DataSet/>}
            </div>
        );
    }

}


