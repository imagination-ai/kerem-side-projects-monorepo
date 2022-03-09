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
    <Grid container spacing={1}>
      <Grid item xs={12}>
        <Typography variant="h4" textAlign={'center'} marginTop="1em">
          Projects
        </Typography>
      </Grid>
      {projects.map((project, i) => (
        <Grid item key={i} xs={12} md={4}>
          <Link to={`/projects/${i + 1}`} style={{ textDecoration: 'none' }}>
            <ActionAreaCard
              description={project.description}
              title={project.title}
              url={project.url}
              key={i}
            />
          </Link>
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
