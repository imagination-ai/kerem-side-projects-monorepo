import { Grid, Box, Typography, Container } from '@mui/material'

export default function Footer() {
  return (
    <footer>
      <Box
        marginTop={'3em'}
        spacing={1}
        p={'1em'}
        sx={{
          backgroundColor: 'primary.dark',
          '&:hover': {
            backgroundColor: 'primary.main',
            opacity: [0.9],
          },
        }}
      >
        <Grid container>
          <Grid item xs={12}>
            <Typography variant={'body2'} align={'center'}>
              Kerem Baskaya © 2021-{new Date().getFullYear()}
            </Typography>
          </Grid>
        </Grid>
      </Box>
    </footer>
  )
}
