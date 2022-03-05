import Grid from '@mui/material/Grid'
import Box from '@mui/material/Box'
import Header from '../Header'
import Sidebar from '../Sidebar'
import { Typography } from '@mui/material'
import Projects from '../Projects/Projects'

export default function Home() {
  return (
    <Box sx={{ flex: 1 }}>
      <Grid container spacing={1}>
        <Grid item xs={12} justifyContent={'center'}>
          <Box>
            <Typography variant="h5" align="center" color="textPrimary">
              Economics | Data Science | Programming
            </Typography>
            <Typography variant="h2" align="center" color="textPrimary">
              Porfolio
            </Typography>
          </Box>
        </Grid>
        <Grid item xs={12} md={9}>
          <Header></Header>
          <Projects />
        </Grid>
        <Grid item xs={12} md={3}>
          <Sidebar></Sidebar>
        </Grid>
      </Grid>
    </Box>
  )
}
