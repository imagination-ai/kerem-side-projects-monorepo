import {
  Container,
  Grid,
  Card,
  CardContent,
  CardActions,
  Typography,
} from '@mui/material'
import React from 'react'
import { Link, Outlet } from 'react-router-dom'
import ActionAreaCard from '../ActionAreaCard/ActionAreaCard'
import projects from '../../lib/utils'

const ProjectLayout = () => {
  return (
    <Grid container spacing={2}>
      <Grid item xs={12}>
        <Typography variant="h4" textAlign={'center'}>
          Projects
        </Typography>
      </Grid>
      {projects.map((project, i) => (
        <Grid item key={i} xs={12} md={6}>
          <ActionAreaCard
            description={project.description}
            title={project.title}
            url={project.url}
            key={i}
          />
        </Grid>
      ))}
    </Grid>
  )
}

export default class Projects extends React.Component {
  render() {
    return <ProjectLayout />
  }
}
