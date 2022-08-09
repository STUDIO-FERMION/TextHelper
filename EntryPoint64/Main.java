
import org.python.core.PySystemState;
import org.python.util.PythonInterpreter;
import org.python.core.PyString;

import java.net.URL;
import java.net.URI;
import java.net.URISyntaxException;
import java.io.File;
import java.io.IOException;
import java.nio.file.Paths;

public class Main {

    public static void main(String[] args) throws IOException, URISyntaxException {

        PythonInterpreter pyProxy = new PythonInterpreter();
        PySystemState pySys = pyProxy.getSystemState();

        URL appURL = Main.class.getResource("TextHelper");

        String appPath;
        if(appURL.getProtocol().equals("jar")){
            String distPath = new File(new URI(appURL.getFile())).getParentFile().getParent();
            appPath = Paths.get(distPath, "TextHelperWin.jar", "TextHelper").toString();
        }
        else{appPath = new File(appURL.getFile()).toString();
        }

        pySys.path.append(new PyString(appPath));

        pyProxy.exec("import EntryPoint");

    };
}
