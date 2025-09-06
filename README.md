# HOML_compiler 1.0.0
# This technology provides the ability to compile a HOML project.

# What is HOML?
HOML (Hyper Object Markup Language) is a new programming language designed for rapid desktop application development. This technology was developed as an alternative to classic desktop applications based on HTML, CSS, JS, and their endless frameworks. The language has an XML-like syntax for ease of adaptation for HTML developers, as well as to improve code readability. As a scripting language, HOML uses C++ and its SDL3 library.

The core idea behind the language is to abandon classic positioning methods using padding, margin, float, and the like. In contrast, UI element positioning in HOML occurs via spatial 2D coordinates (x, y), which allows for greater creative freedom in complex designs. The use of a coordinate system also simplifies complex graphic effects, transitions, and the movement of elements on the page.

As of August 2025, HOML can only be compiled to C++ SDL3, providing excellent application performance. However, this requires developers to have a good understanding of one of the most complex programming languages. It also makes it difficult to track errors during compilation, as configuring a preprocessor to analyze C++ code for errors is extremely challenging. Future plans include adding Python as a scripting language and the ability to compile HOML projects into PyFlet applications. It's also considered possible to add a custom HOML_script scripting language, specifically optimized for UI element management, and capable of compiling to both C++ SDL3 and Python PyFlet.

# How to install HOML for Windows?
You can install HOML using the installer.exe file:
1. Download the installer.exe file from the repository.
2. Run the file as an administrator.
3. Accept the user agreement.
4. Specify the installation path for HOML.
5. Click "Install"

If you have correctly performed the above steps, the path to the Homl/bin folder will be added to the system's Path environment variable, and you can access `homl` from any directory in the terminal to execute the desired command.

# How to use HOML in terminal?
To use the HOML toolkit, open the command prompt (preferably as an administrator) and, from any directory on the drive where you installed the compiler, type `homl` to access its features:
Properties:
    --version: print out homl version;

Commands:
    compile: compile your homl project; Args: –path
    create: create new homl project; Args: –language, –path

# HOML language documentation
The language has an XML-like syntax and a structure that strongly resembles HTML. The fundamental unit of a HOML project is the `main.homl` file, from which all external folders, libraries, pages, and other components are included.

```
<homl doctype="__main__">
  <inf>
    <id>HomlProject</id>

    <language>Cpp</language>
    
    <width>1920</width>
    <height>1080</height>

    <lib>homl</lib>
    <lib>project</lib>

    <dir>assets</dir>
  </inf>
  
  <content>
    <page ismain="true">enter.homl</page>
  </content>
</homl>
```

<homl> - is the main tag of any HOML document (applicable to HOML documents with any doctype value).
Attributes:
    doctype - defines the type of HOML document.
    Values:
    	"__main__"  - HOML project
        "__page__"  - HOML page
        "__var__"   - HOML variable
        "__el__"    - HOML element
        "__lib__"   - HOML library
        "__class__" - HOML class

Nested tags:
    <inf> - is a tag describing the properties of a HOML document (applicable to HOML documents with any doctype value).
    Nested tags:
        <id> - contains the ID of the HOML document. It should match the file name if the document is a separate file (applicable to HOML documents with any doctype value. Required for all HOML documents except doctype="__var__", "__el__", "__code__", "__any__").
        Examples:
            <id>HomlProject</id>

        <lib> - contains the path/text of a HOML library document (applicable to HOML documents with doctype="__main__").
        Examples:
            Recommended example:
                <lib>lib.homl</lib>

                lib.homl:
                    <homl doctype="__lib__">
                      <inf>
                        <id>example_lib</id>
                      </inf>
                            
                      <content>
                        <file>file1.homl</file>
                        <file>file2.homl</file>
                      </content>
                    </homl>

                The code lib-document is located in an external file, with value doctype = "__lib__". The tag <lib> contains path to this file.

            OR

            Unrecommended example:
                <lib>"<homl doctype=\"__lib__\"><inf>...</content></homl>"<lib>

                The code lib-document is located in tag <lib>

        <dir> - contains the path to a folder included in the project's dist directory (applicable to HOML documents with doctype="__main__").
        Examples:
            <dir>assets/images</dir>

        <language> - contains the name of the language being used (applicable to HOML documents with doctype="__main__". Required for HOML documents with the "__main__" doctype).
        Examples:
            <language>Cpp<language>

        <width> - contains information about the width of the application window (applicable to HOML documents with doctype="__main__". Required for HOML documents with the "__main__" doctype).
        Examples:
            <width>1920</width>

        <height> - contains information about the height of the application window (applicable to HOML documents with doctype="__main__". Required for HOML documents with the "__main__" doctype).
        Examples:
            <height>1080</height>

        <bg> - contains the path/RGBA color of the page background (applicable to HOML documents with doctype="__page__". Required for HOML documents with the "__page__" doctype).
        Examples:
            <bg>assets/images/background.jpg</bg>

            OR

            <bg>{255, 255, 255, 255}</bg>

    <content> - is a tag describing the content of a HOML document (applicable to HOML documents with any doctype value).
    Nested tags:
        <page> - contains the path/text of a HOML page document (applicable to HOML documents with doctype="__main__").
        Attributes:
            ismain - determines whether the page is the main page.
            Values: true/false

        Examples:
            Recommended example:
                <page>enter.homl</page>

                enter.homl:
                    <homl doctype="__page__">
                      <inf>
                        <id>Enter</id>
                        <bg>{255, 255, 255, 255}</bg>
                      </inf>
                        
                      <content>
                        <el type="Label">(id="example_el")</el>
                        <var type="string">word = "Hello, world!"</var>

                        <init>enter_init.homl</init>

                        <update>enter_update.homl</update>

                        <loop>"if (Enter.is_active()) { Enter.update(); Enter.draw(); } // Global logic about this page"</loop>

                      </content>
                    </homl>

            Unrecommended example:
                <page>"<homl doctype=\"__page__\"><inf>...</content></homl>

        <var> - contains the path/document-text/tag-content-text of a variable tag of the application/page (applicable to HOML documents with doctypes "__main__", "__page__").
        Attributes:
            type - defines the type of variable.

            Recommended example:
                <var type="int">num = 69</var>

            Unrecommended example:
                <var type="int">"
                  <homl doctype="__var__">
                    <content>num = 69</content>
                  </homl>
                "</var>

            Unrecommended example:
                <var type="int">variable.homl</var>

                variable.homl:
                    <homl doctype="__var__">
                      <content>num = 69</content>
                    </homl>

        <el> - contains the path/document-text/tag-content-text of an element tag of the page (applicable to HOML documents with doctype="__page__").
        Attributes:
            type - defines the type of element.

            Recommended example:
                <el type="Label">(id="example_label", text="Hello, world!")</el>

            Unrecommended example:
                <el type="Label">"
                  <homl doctype="__el__">
                    <content>(id="example_label", text="Hello, world!")</content>
                  </homl>
                "</el>

            Unrecommended example:
                <el type="Label">element.homl</var>

                element.homl:
                    <homl doctype="__el__">
                      <content>(id="example_label", text="Hello, world!")</content>
                    </homl>

        <init> - contains the application initialization logic code (applicable to HOML documents with doctype="__page__")
        Recommended example:
            <init>init_logic.homl</init>

            init_logic.homl:
                <homl doctype="__code__">
                  <content>
                    print("Hello, world!") // Initialization logic
                  </content>
                </homl>

        Unrecommended example:
            <init>"
              <homl doctype="__code__">
                <content>
                  print("Hello, world!") // Initialization logic
                </content>
              </homl>
            "</init>

        Unrecommended example:
            <init>
              print("Hello, world!") // Initialization logic
            </init>

        <update> - contains the application update logic code (applicable to HOML documents with doctype="__page__")
        Recommended example:
            <update>update_logic.homl</update>

            update_logic.homl:
                <homl doctype="__code__">
                  <content>
                    print("New frame!") // Updating logic
                  </content>
                </homl>

        Unrecommended example:
            <update>"
              <homl doctype="__code__">
                <content>
                  print("New frame!") // Updating logic
                </content>
              </homl>
            "</update>

        Unrecommended example:
            <update>
              print("New frame!") // Updating logic
            </update>

        <loop> - contains the application global loop logic code (applicable to HOML documents with doctype="__page__")
        Recommended example:
            <loop>
              if (Enter.is_active()) { Enter.update(); Enter.draw(); } // Global logic about this page
            </loop>

        Unrecommended example:
            <loop>"
              <homl doctype="__code__">
                <content>
                  if (Enter.is_active()) { Enter.update(); Enter.draw(); } // Global logic about this page
                </content>
              </homl>
            "</loop>

        Unrecommended example:
            <loop>loop_logic.homl</loop>

            loop_logic.homl:
                <homl doctype="__code__">
                  <content>
                    if (Enter.is_active()) { Enter.update(); Enter.draw(); } // Global logic about this page
                  </content>
                </homl>
