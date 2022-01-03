import React, { Component } from 'react'

import Aux from '../../hoc/Aux/Aux'
import classes from './Layout.module.css'
// import Toolbar from '../../components/Navigation/Toolbar/Toolbar';
import SideDrawer from '../../components/Navigation/SideDrawer/SideDrawer'

class Layout extends Component {
  state = {
    showSideDrawer: true
  }

  sideDrawerClosedHandler = () => {
    this.setState({ showSideDrawer: false })
  }

  sideDrawerToggleHandler = () => {
    this.setState(prevState => {
      return { showSideDrawer: !prevState.showSideDrawer }
    })
  }

  render () {
    return (
      <Aux>
        <div className={classes.container}>
          <div className={classes.header}>
            <h1 className={classes.title}>Kerem Baskaya Project blog</h1>
          </div>
          <div className={classes.aside}>
            <SideDrawer
              open={this.state.showSideDrawer}
              closed={this.sideDrawerClosedHandler}
            />
          </div>
          <div className={classes.content}>{this.props.children}</div>
          {/* {<div className={classes.container.footer}>aasdfasdf</div>} */}
          <div className={classes.footer}>Kerem Baskaya © 2022</div>
        </div>
      </Aux>
    )
  }
}

export default Layout
