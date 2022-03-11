import { Typography } from '@mui/material'
import Link from 'react-router-dom'

export default function LinkToMainPage() {
  return (
    <Link
      to="/"
      style={{
        textDecoration: 'none',
        color: 'white',
      }}
    >
      <Typography
        variant="h6"
        noWrap
        component="div"
        sx={{ mr: 2, display: { xs: 'none', md: 'flex' } }}
      >
        Kerem - Blog
      </Typography>
    </Link>
  )
}
