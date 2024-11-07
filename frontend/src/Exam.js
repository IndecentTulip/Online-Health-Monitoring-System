
//navigation menu
import { useNavigate } from 'react-router-dom';
//Tracking the information filled out on the form.
import React, { useEffect, useState } from 'react';
// if docter decides to prescribe an exam for patients
import './DoctorMain';
 // import exam css styles
import './Exam.css';

//retrieving info from the database
import axios from 'axios';

const Exam = () =>{
    
    //Doctor can nvigate around the exam menu.
    const navigate = useNavigate();
    
    // set variables from form
    const[examId, setExamID] = useState('')
    const[patientId, setPatientID] = useState('');
    const[content, setContent] = useState(''); 

    //if user decides to prescribe exam
    if (Exam.prescribe){
           //Form to fill out the info.
           <form>
            <input
            type = "text"
            value = {examID}
            onChange={(e) => setExamID(e.target.value)}
            placeholder="Email"
            required/>
           </form>
    }//if

    //form handling 
    const

    //Storing prescribed exams in the database. 
   try {
       await axios.post('http://localhost:5000/exam',{
       examId,
       patientId,
       content
       });
   }//try
   catch(err){


   }
   
}//Exam