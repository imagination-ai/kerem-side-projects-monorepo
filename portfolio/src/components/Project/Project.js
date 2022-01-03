import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import MarkdownTranslator from '../MarkdownTranslator/MarkdownTranslator'
import { getProject } from '../Projects/Projects'
import StyleClient from '../../utils/style/style_client'
import axios from 'axios'

const client = new StyleClient(
  process.env.REACT_APP_STYLE_HOST || 'localhost',
  process.env.REACT_APP_STYLE_PORT || '8080'
)

export default function Project (props) {
  let params = useParams()
  let project = getProject(parseInt(params.projectId, 10))

  const [predictions, setPredictions] = useState()
  const [inputField, setInputField] = useState({
    text: '',
    model_name: ''
  })

  const inputsHandler = e => {
    const { name, value } = e.target
    setInputField(prevState => ({
      ...prevState,
      [name]: value
    }))
  }

  const handlePredictions = async () => {
    console.log(
      'Handling predictions with ' +
        inputField.text +
        ' ' +
        inputField.model_name
    )
    const results = await client.predict(inputField.text, inputField.model_name)
    setPredictions(JSON.stringify(results.data['prediction']))
  }

  return (
    <div>
      <h1>{project.title}</h1>
      <div> {project.description}</div>
      Text: {inputField.text}, Model Name: {inputField.model_name}
      <div>Here some predictions: {predictions}</div>
      {/* <MarkdownTranslator /> */}
      <div>
        <input
          type='text'
          name='text'
          onChange={inputsHandler}
          placeholder='Text?'
          value={inputField.text}
        />

        <br />

        <input
          type='text'
          name='model_name'
          onChange={inputsHandler}
          placeholder='Model Name?'
          value={inputField.model_name}
        />

        <br />

        <button onClick={handlePredictions}>Submit Now</button>
      </div>
    </div>
  )
}
