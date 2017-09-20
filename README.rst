Jarbas DSL is a small Domain Specific Language to describe interactions between
the user and the computer in a command line interface. It is designed to be used
in the Jarbas project, but it might also be useful elsewhere.

In Jarbas DSL, we assume that all interactions are executed associated with a
namespace. The execution might read variable names in the namespace and change
them based on user input. Here is a small example::

    Hello $name! Welcome to Jarbas.

This piece extracts the name variable from the namespace and substitute it 
inplace. If the variable does not exist, it raises an error.

The dollar sign represents a variable substitution. Jarbas DSL accepts small 
transformations followed by the dollar sign::

    Hello $person.name!     // attribute access
    Hello $name.title()!    // method calling
    Hello $name|title!      // the pipe operator (applies the title filter to name)

By the way, *"//"* mark comments. 


User input
==========

Of course there is no meaningful human computer interaction if we can only show
strings on the screen. In Jarbas DSL, we can ask for user input using the square
bracket syntax:

    Name: [name]
    Hello $name!

The above interaction asks for the user name and saves the result as a string 
in the name variable. We can also specify more complex input as in the examples::

    Name: [name]            // string input
    Age: [age=int]          // integer input
    Email: [email=&email]   // validates with the email function passed by the user
    Github: [github=@email] // Ask for input, but uses email as default value

Conditional execution
=====================

Jarbas also accepts conditional execution of instructions::

    =if $is_minor(age)
    You cannot proceed.
    =elif Do you want to proceed? [proceed=bool]
    Ok, let's go!
    =else
    Bye!
    =endif
