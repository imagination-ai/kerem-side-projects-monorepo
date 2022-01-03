import React from 'react'
import classes from './ProjectCard.module.css'
import image from '../../assets/images/shakespeare.jpeg';

export default class ProjectCard extends React.Component {
  render () {
    return (
      <div className={classes.card}>
        <h1>{this.props.title}</h1>
        <p>{this.props.description}</p>
        <div className={classes.visual}>
          <img src={image} alt='Stuff' />
        </div>
      </div>
    )
  }
}
