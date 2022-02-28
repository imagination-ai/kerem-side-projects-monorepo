import Grid from '@mui/material/Grid'
import Box from '@mui/material/Box'
import Header from '../Header'
import Sidebar from '../Sidebar'

export default function Home() {
  return (
    <Box sx={{ flexGrow: 1 }}>
      <Grid container spacing={2}>
        <Grid item xs={9}>
          <Header></Header>
        </Grid>
        <Grid item xs={3}>
          <Sidebar></Sidebar>
        </Grid>
      </Grid>
    </Box>
  )
}
