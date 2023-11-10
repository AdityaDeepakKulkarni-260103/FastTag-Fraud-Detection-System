import React, { useState } from 'react'
import HeaderComp from './HeaderComp'
import FooterComp from './FooterComp'

const StepTwoA = ({setStepOneOpen,stepTwoAOpen,setStepTwoAOpen,setStepThreeAOpen,setStepFourSOpen,setImage,image,getData,setError,error}) => {

    const [imgPreview, setImgPreview] = useState(null)

    const selelectedFileHandler = async (e) => {
        setImage(e.target.files[0])
        setImgPreview(URL.createObjectURL(e.target.files[0]))
    }

    const uploadImage = () => {
        if (image) {
            setError(null)
            getData()
        } else {
            setError('No image Selected')
        }
    }

    if (stepTwoAOpen) {
        return (
            <div className="stepContainer">
                <HeaderComp tittleText={"Upload Image"} descriptionText={"Upload Image to charge toll"} />
                <div className="stepContent">
                    <input type="file" onChange={selelectedFileHandler} />
                    <div className="imgPreview">
                        <img className="previewImg" src={imgPreview} alt="PreviewImage" />
                    </div>
                    <div className="uploadButton" onClick={uploadImage}>
                        <svg width="18" height="19" viewBox="0 0 18 19" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M9 2L13.3333 6M9 2L5 6M9 2V14.6667M17 9.33333V18H1V9.33333" stroke="black" stroke-width="2"/>
                        </svg>
                        <div>
                            Upload Image
                        </div>
                    </div>
                </div>
                <FooterComp error={error} setError={setError} previousPageText={"Go Back"} nextPageText={"Next"} previousPage={setStepOneOpen} currentPage={setStepTwoAOpen} />
            </div>
          )   
    } else {
        return(null)
    }
}

export default StepTwoA