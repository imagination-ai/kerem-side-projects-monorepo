import React from 'react'
import NavigationItem from './NavigationItem/NavigationItem'
import classes from './NavigationItems.css'

const navigationItems = props => (
  <ul className={classes.NavigationItems}>
    <NavigationItem link='/'>Home</NavigationItem>
    <NavigationItem link='/projects'>
      Projects
    </NavigationItem>
    <NavigationItem link='/about'>About</NavigationItem>
  </ul>
)

export default navigationItems
