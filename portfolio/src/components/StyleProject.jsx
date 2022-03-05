import React, { useState } from 'react'
import { useParams } from 'react-router-dom'
import StyleClient from '../client/style_client'
import Form from 'react-bootstrap/Form'
import 'bootstrap/dist/css/bootstrap.min.css'
import Button from '@mui/material/Button'
import Table from 'react-bootstrap/Table'

import Grid from '@mui/material/Grid'
import Box from '@mui/material/Box'
import Typography from '@mui/material/Typography'
import Card from '@mui/material/Card'
import CardContent from '@mui/material/CardContent'
import {
  CardActionArea,
  Chip,
  FormControlLabel,
  FormGroup,
  FormLabel,
  Link,
  Radio,
  RadioGroup,
  Stack,
  TextField,
} from '@mui/material'
import Divider from '@mui/material/Divider'
import InterestList from './InterestList'

const client = new StyleClient(
  process.env.REACT_APP_STYLE_HOST || 'localhost',
  process.env.REACT_APP_STYLE_PORT || '8080',
)

// export function getProject (index) {
//   return projects[index]
// }

export default function StyleProject(props) {
  let params = useParams()
  // let project = getProject(parseInt(params.projectId, 10))

  const [predictions, setPredictions] = useState({})
  const [inputField, setInputField] = useState({
    text: '',
    model_name: 'mock',
  })

  const inputsHandler = (e) => {
    const { name, value } = e.target
    setInputField((prevState) => ({
      ...prevState,
      [name]: value,
    }))
  }

  const predictionToTable = (prediction) => {
    return (
      <tbody>
        {Object.entries(predictions).map(([key, value]) => {
          // console.log(key, value)
          return (
            <tr key={key}>
              <td></td>
              <td>{key}</td>
              <td>{value}</td>
            </tr>
          )
        })}
      </tbody>
    )
  }

  const handlePredictions = async () => {
    console.log(inputField.text)
    const results = await client.predict(inputField.text, inputField.model_name)
    setPredictions(results.data['prediction'])
    // setPredictions(JSON.stringify(results.data['prediction']))
  }

  return (
    <Box sx={{ flex: 1 }} m={4}>
      <Grid container spacing={1}>
        <Grid item xs={12}>
          <Typography variant="h2" textAlign={'left'}>
            {props.project.title}
          </Typography>
        </Grid>
        <Grid item xs={9}>
          <Typography variant="h5" component="p">
            {props.project.description}
          </Typography>
        </Grid>
        <Grid item xs={3}>
          <Typography
            variant="h5"
            weight="200"
            fontSize="10px"
            textAlign={'right'}
          >
            2022, March 3
          </Typography>
        </Grid>
        <Grid item xs={12}>
          <Box
            component="img"
            sx={{
              height: 350,
              width: '100%',
              objectFit: 'cover',
              //   width: 350,
              //   maxHeight: { xs: 233, md: 167 },
              //   maxWidth: { xs: 350, md: 250 },
            }}
            alt=""
            src={props.project.url}
          />
        </Grid>
        <Grid item xs={12} marginBottom={'4rem'}>
          <Card>
            <CardActionArea>
              <CardContent
                style={{
                  display: 'flex',
                  gap: '1rem',
                  height: '100%',
                }}
              >
                <Link href={props.project.repo_url}>Repo @ Github</Link>

                <Divider orientation="vertical"></Divider>

                <Stack
                  direction="row"
                  style={{ flexWrap: 'wrap', gap: '0.5rem' }}
                >
                  {props.project.tags.map((tag, i) => (
                    <Chip label={tag} key={i} p={2} color="primary" />
                  ))}
                </Stack>
              </CardContent>
            </CardActionArea>
          </Card>
        </Grid>

        {/* <h1>{props.project.title}</h1>
      <div>
        <br></br>
        <i> {props.project.description}</i>
      </div>
      <br></br>
      <p>
        What we do In this project, we created a few models with different sizes
        each of which take text as input, and returns a list of of authors. The
        bigger the probability, the closer the style of the corresponding
        author. Currently, we return only the <b>top 3 authors</b>.
      </p> */}

        <Grid item xs={12} md={8} paddingRight={2}>
          <Typography>
            Lorem ipsum dolor, sit amet consectetur adipisicing elit. Adipisci
            eaque sint accusantium! Dolorum eligendi distinctio dolores maxime
            expedita veniam perferendis dolor necessitatibus nisi animi nam illo
            suscipit sunt, consequatur quia. Lorem, ipsum dolor sit amet
            consectetur adipisicing elit. Sit tempora cumque iste perferendis
            vitae hic excepturi exercitationem culpa molestiae porro distinctio
            autem numquam dolor unde a, illo impedit commodi nulla! Lorem ipsum
            dolor, sit amet consectetur adipisicing elit. Adipisci eaque sint
            accusantium! Dolorum eligendi distinctio dolores maxime expedita
            veniam perferendis dolor necessitatibus nisi animi nam illo suscipit
            sunt, consequatur quia. Lorem, ipsum dolor sit amet consectetur
            adipisicing elit. Sit tempora cumque iste perferendis vitae hic
            excepturi exercitationem culpa molestiae porro distinctio autem
            numquam dolor unde a, illo impedit commodi nulla! Lorem ipsum dolor,
            sit amet consectetur adipisicing elit. Adipisci eaque sint
            accusantium! Dolorum eligendi distinctio dolores maxime expedita
            veniam perferendis dolor necessitatibus nisi animi nam illo suscipit
            sunt, consequatur quia. Lorem, ipsum dolor sit amet consectetur
            adipisicing elit. Sit tempora cumque iste perferendis vitae hic
            excepturi exercitationem culpa molestiae porro distinctio autem
            numquam dolor unde a, illo impedit commodi nulla! Lorem ipsum dolor,
            sit amet consectetur adipisicing elit. Adipisci eaque sint
            accusantium! Dolorum eligendi distinctio dolores maxime expedita
            veniam perferendis dolor necessitatibus nisi animi nam illo suscipit
            sunt, consequatur quia. Lorem, ipsum dolor sit amet consectetur
            adipisicing elit. Sit tempora cumque iste perferendis vitae hic
            excepturi exercitationem culpa molestiae porro distinctio autem
            numquam dolor unde a, illo impedit commodi nulla! Lorem ipsum dolor,
            sit amet consectetur adipisicing elit. Adipisci eaque sint
            accusantium! Dolorum eligendi distinctio dolores maxime expedita
            veniam perferendis dolor necessitatibus nisi animi nam illo suscipit
            sunt, consequatur quia. Lorem, ipsum dolor sit amet consectetur
            adipisicing elit. Sit tempora cumque iste perferendis vitae hic
            excepturi exercitationem culpa molestiae porro distinctio autem
            numquam dolor unde a, illo impedit commodi nulla! epturi
          </Typography>
          <Typography marginTop={1}>
            exercitationem culpa molestiae porro distinctio autem numquam dolor
            unde a, illo impedit commodi nulla! Lorem ipsum dolor, sit amet
            consectetur adipisicing elit. Adipisci eaque sint accusantium!
            Dolorum eligendi distinctio dolores maxime expedita veniam
            perferendis dolor necessitatibus nisi animi nam illo suscipit sunt,
            consequatur quia. Lorem, ipsum dolor sit amet consectetur
            adipisicing elit. Sit tempora cumque iste perferendis vitae hic
            excepturi exercitationem culpa molestiae porro distinctio autem
            numquam dolor unde a, illo impedit commodi nulla!
          </Typography>
        </Grid>

        <Grid
          item
          xs={12}
          md={4}
          style={{
            position: 'sticky',
            top: '0',
            height: 'fit-content',
            display: 'flex',
            flexDirection: 'column',
          }}
        >
          <Typography variant="h5" height="68.5px">
            You can try by yourself!
          </Typography>

          <Table striped bordered hover>
            <thead>
              <tr>
                <th>#</th>
                <th>Author</th>
                <th>Probability</th>
              </tr>
            </thead>
            {predictionToTable(predictions)}
          </Table>

          <Form>
            {/* <Form.Group className="mb-3" controlId="formBasicEmail">
              <Form.Label>
                Jot down or copy some text. We can tell you wrote this!
              </Form.Label>
              <Form.Control
                // type='email'
                name="text"
                value={inputField.text}
                onChange={inputsHandler}
                placeholder="It was the best of times, it was the worst of times..."
              />
              <Form.Text className="text-muted">
                Copy or write some snippet to figure out who would be the
                author...
              </Form.Text>
            </Form.Group> */}

            <Box
              component="form"
              sx={{
                '& > :not(style)': { m: 1, width: '25ch' },
              }}
              noValidate
              autoComplete="off"
            >
              <TextField
                required
                multiline={true}
                id="outlined-uncontrolled"
                name="text"
                label="Jot down here"
                value={inputField.text}
                onChange={inputsHandler}
              />
            </Box>

            <br></br>

            <FormLabel id="demo-radio-buttons-group-label">Gender</FormLabel>
            <RadioGroup
              aria-labelledby="demo-radio-buttons-group-label"
              defaultValue="mock"
              name="model_name"
            >
              <FormControlLabel
                value="small"
                control={<Radio />}
                label="Small Model"
                onChange={inputsHandler}
              />
              <FormControlLabel
                value="mock"
                control={<Radio />}
                label="Mock Model"
                onChange={inputsHandler}
              />
            </RadioGroup>

            {/* <Form.Group className="mb-3" controlId="formBasicPassword">
              <Form.Select
                aria-label="Default select example"
                name="model_name"
                value={inputField.model_name}
                onChange={inputsHandler}
              >
                <option value="small">small-model</option>
                <option value="mock">mock-model</option>
              </Form.Select>
            </Form.Group> */}

            <Button variant="contained" onClick={handlePredictions}>
              Guess who I am!
            </Button>
          </Form>
        </Grid>
      </Grid>
    </Box>
  )
}
