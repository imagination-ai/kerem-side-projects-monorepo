import React, { useState } from 'react'
import StyleClient from '../client/style_client'
import Form from 'react-bootstrap/Form'
import Button from '@mui/material/Button'
import Table from 'react-bootstrap/Table'

import Grid from '@mui/material/Grid'
import Box from '@mui/material/Box'
import Typography from '@mui/material/Typography'
import {
  FormControlLabel,
  FormLabel,
  Radio,
  RadioGroup,
  TextField,
} from '@mui/material'
import ProjectWithCode from './ProjectWithCode'
import ModelDetailsDialog from './ModelDetailsDialog'

const client = new StyleClient(
  process.env.REACT_APP_STYLE_HOST || 'localhost',
  process.env.REACT_APP_STYLE_PORT || '8080',
)

let modelDetails = {
  mock:
    'This model is just a mock model. It is not a real model and always returns the same thing.',
  small: 'This model is based on Logistic Regression and TFIDFVectorizer. ',
}

export default function StyleProject(props) {
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
    <ProjectWithCode
      project={props.project}
      text={` More to come.`}
      date="2022, March 3"
      code={
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

            <FormLabel id="demo-radio-buttons-group-label">Model Names</FormLabel>
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

            <Box style={{ display: 'flex', gap: '1rem' }}>
              <Button variant="contained" onClick={handlePredictions}>
                Guess who I am!
              </Button>
              <ModelDetailsDialog
                model_name={inputField.model_name}
                text={modelDetails[inputField.model_name]}
              />
            </Box>
          </Form>
        </Grid>
      }
    ></ProjectWithCode>
  )
}
