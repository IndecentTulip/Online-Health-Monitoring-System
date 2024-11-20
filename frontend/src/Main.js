import './Main.css';
import { useNavigate } from 'react-router-dom';
import logo from './logo_processed.png';

const Main = () => {
  const navigate = useNavigate();

  const handleNavigation = (path) => {
    navigate(path); 
  };

  return (
    <div className="background">
      <div className="navbarname">
        Jlabs
      </div>
      <nav className="navbar">
        <img src={logo} alt="logo" className="logo" />
        <button className="register" onClick={() => handleNavigation('/register')}>Register</button>
        <button className="signin" onClick={() => handleNavigation('/signin')}>Sign In</button>
      </nav>

      {/* Quote Container for About Us section */}
      <div className="main-quote-container">
        <div className="main-quote-open">“</div>
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
          </p>
        </div>
        <div className="main-quote-close">”</div>
      </div>
    </div> 
  );
}
export default Main;

