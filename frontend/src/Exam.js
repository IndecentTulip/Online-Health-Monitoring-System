
//navigation menu
import { useNavigate } from 'react-router-dom';
// if docter decides to prescribe an exam for patients
import './DoctorMain';

//retrieving info from the database
import axios from 'axios';

const Exam = () =>{
    
    //Doctor can nvigate around the exam menu.
    const navigate = useNavigate();
    
    //if user decides to prescribe exam
    if (Exam.prescribe){
        <form>
            var examID = readline("Enter examID");
            var patientID = readline ("Enter patientID");
            var content = readline ("Describe the exam"); 
        </form>
    }//if
}

class prescribe{
     
    //refers to patient information to itself. 
     examID(examId, patientId, content){
        this.examID
        this.patientId
        this.content
    }//examID

}//Prescribe