import './Main.css';
import { useNavigate } from 'react-router-dom';

const Main = () => {
  const navigate = useNavigate();

  const handleRedirect = () => {
    navigate('/signin'); 
  };

  const handleNavigation = (path) => {
    navigate(path); 
  };

  return (
    <div>
<div className = "background"></div>
<div className="navbarname">
          Jlabs
        </div>
<nav className="navbar">
        <button onClick={() => handleNavigation('/Main')}>Home</button>
        <button onClick={() => handleNavigation('/register')}>Register</button>
        <button onClick={() => handleNavigation('/signin')}>Sign In</button>
       </nav>

       <div className="about-section"> 
     <h1>About Us</h1>
     <p> Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
      Etiam porttitor bibendum massa, eget consectetur justo porttitor vel. 
      Aliquam dictum id dui laoreet consectetur. Suspendisse non nibh vel metus varius rhoncus non at orci. 
      Praesent non dapibus justo, et aliquam eros. Duis et lobortis neque. Curabitur sit amet tempor lectus. 
      Quisque sollicitudin ipsum nec mi condimentum, ac eleifend ante accumsan.Praesent a leo ultrices, condimentum lectus a, viverra diam.
      Aliquam non lorem quis dui elementum semper in vitae leo. Phasellus mattis, massa sit amet varius imperdiet, purus neque tincidunt arcu,
      id fringilla neque tellus ac eros. Maecenas quis tempus est, in ornare augue. Vestibulum tempor velit eget aliquet efficitur. 
      Aenean sollicitudin nulla non rutrum lacinia. Mauris lacinia augue molestie, vestibulum turpis id, porta quam. Morbi semper suscipit porta. 
      Suspendisse at lacus commodo, pharetra augue quis, dapibus tortor. Donec non egestas quam. Nam mattis arcu lacus, id sagittis nunc molestie ut.
      Sed condimentum libero id pellentesque condimentum.Etiam bibendum felis eget nulla posuere, vitae lacinia turpis convallis. 
      Sed pharetra, lectus id pretium accumsan, lacus ipsum. </p>

    </div> 
  </div>
  );
}
export default Main;    