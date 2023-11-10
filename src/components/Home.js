import React, { useState } from 'react'
import './home.css'
import StepOne from './StepOne'
import StepTwoA from './StepTwoA'
import StepFourS from './StepFourS'
import axios from 'axios'
import StepFourL from './StepFourL'

export const Home = () => {

    const [stepOneOpen, setStepOneOpen] = useState(true)
    const [stepTwoAOpen, setStepTwoAOpen] = useState(false)
    const [stepThreeAOpen, setStepThreeAOpen] = useState(false)
    const [stepFourSOpen, setStepFourSOpen] = useState(false)
    const [stepFourLOpen, setStepFourLOpen] = useState(false)
    const [vehicleDetails, setVehicleDetails] = useState(null)
    const [vehicleDetailsL, setVehicleDetailsL] = useState(null)
    const [error, setError] = useState('')
    const [image, setImage] = useState(null)
    const [imgPreview, setImgPreview] = useState(null)

    const getData = async () => {
       const data = await axios.post('http://127.0.0.1:5000/getdata',{
        name: image.name
       })
       console.log(data.data);
      setVehicleDetails(data.data)
      if (vehicleDetails) {
        setImgPreview(URL.createObjectURL(image))
        setStepTwoAOpen(false)
        setStepFourSOpen(true)
      } else {
        setError('Invalid Registration')
      }
    }

    const openStepTwoA = () => {
      setStepOneOpen(false)
      setStepTwoAOpen(true)
    }

    const openStepFourL = async () => {

      const data = await axios.get('http://127.0.0.1:5000/getdata')
      setVehicleDetailsL(data.data)
      setStepOneOpen(false)
      setStepTwoAOpen(false)
      setStepFourLOpen(true)

    }

    return (
    <div className="mainContainer">
        <StepOne openStepTwoA ={openStepTwoA} openStepFourL={openStepFourL} stepOneOpen={stepOneOpen} setImgPreview={setImgPreview} setStepOneOpen={setStepOneOpen} stepTwoAOpen={stepTwoAOpen} setStepTwoAOpen={setStepTwoAOpen} error={error} setError={setError} />
        <StepTwoA setImage={setImage} image={image} stepOneOpen={stepOneOpen} setStepOneOpen={setStepOneOpen} stepTwoAOpen={stepTwoAOpen} setStepTwoAOpen={setStepTwoAOpen} stepThreeAOpen={stepThreeAOpen} setStepThreeAOpen={setStepThreeAOpen} stepFourSOpen={stepFourSOpen} setStepFourSOpen={setStepFourSOpen} getData={getData} error={error} setError={setError} />
        <StepFourS setImage={setImage} image={imgPreview} stepOneOpen={stepOneOpen} setStepOneOpen={setStepOneOpen} stepTwoAOpen={stepTwoAOpen} setStepTwoAOpen={setStepTwoAOpen} stepFourSOpen={stepFourSOpen} setStepFourSOpen={setStepFourSOpen} vehicleDetails={vehicleDetails} setVehicleDetails={setVehicleDetails} error={error} setError={setError} />
        <StepFourL stepOneOpen={stepOneOpen} setStepOneOpen={setStepOneOpen} stepTwoAOpen={stepTwoAOpen} setStepTwoAOpen={setStepTwoAOpen} stepFourLOpen={stepFourLOpen} setStepFourLOpen={setStepFourLOpen} vehicleDetails={vehicleDetailsL} error={error} setError={setError} />
    </div>
  )
}