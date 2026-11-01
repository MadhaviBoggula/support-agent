import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

// ============================================================
// API URL
// ============================================================

const String baseUrl = "http://127.0.0.1:8000";

// ============================================================
// MAIN
// ============================================================

void main() {
  runApp(const MyApp());
}

// ============================================================
// APP
// ============================================================

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: "Secure Login",
      theme: ThemeData(useMaterial3: true, fontFamily: "Arial"),
      home: const LoginPage(),
    );
  }
}

// ============================================================
// LOGIN PAGE
// ============================================================

class LoginPage extends StatefulWidget {
  const LoginPage({super.key});

  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final emailController = TextEditingController();
  final passwordController = TextEditingController();

  bool loading = false;
  bool obscurePassword = true;

  String message = "";
  bool loginSuccess = false;

  // ==========================================================
  // LOGIN
  // ==========================================================

  Future<void> login() async {
    if (emailController.text.trim().isEmpty ||
        passwordController.text.isEmpty) {
      setState(() {
        message = "Please enter email and password";
        loginSuccess = false;
      });

      return;
    }

    setState(() {
      loading = true;
      message = "";
    });

    try {
      final response = await http
          .post(
            Uri.parse("$baseUrl/login"),

            headers: {"Content-Type": "application/json"},

            body: jsonEncode({
              "email": emailController.text.trim(),
              "password": passwordController.text,
            }),
          )
          .timeout(const Duration(seconds: 15));

      print("LOGIN STATUS: ${response.statusCode}");
      print("LOGIN RESPONSE: ${response.body}");

      final data = jsonDecode(response.body);

      if (response.statusCode == 200) {
        final token = data["access_token"];

        await getProfile(token);
      } else {
        setState(() {
          message = data["detail"] ?? "Login failed";

          loginSuccess = false;
        });
      }
    } catch (e) {
      print("LOGIN ERROR: $e");

      setState(() {
        message = "Connection error:\n$e";
        loginSuccess = false;
      });
    } finally {
      setState(() {
        loading = false;
      });
    }
  }

  // ==========================================================
  // GET PROFILE
  // ==========================================================

  Future<void> getProfile(String token) async {
    try {
      final response = await http
          .get(
            Uri.parse("$baseUrl/profile"),

            headers: {"Authorization": "Bearer $token"},
          )
          .timeout(const Duration(seconds: 15));

      final data = jsonDecode(response.body);

      if (response.statusCode == 200) {
        final user = data["user"];

        setState(() {
          message =
              "Welcome, ${user["name"]}!\n\n"
              "Email: ${user["email"]}\n"
              "Mobile: ${user["mobile"]}";

          loginSuccess = true;
        });
      } else {
        setState(() {
          message = data["detail"] ?? "Invalid token";

          loginSuccess = false;
        });
      }
    } catch (e) {
      setState(() {
        message = "Profile error:\n$e";

        loginSuccess = false;
      });
    }
  }

  // ==========================================================
  // INPUT DECORATION
  // ==========================================================

  InputDecoration inputDecoration({
    required String label,
    required IconData icon,
  }) {
    return InputDecoration(
      labelText: label,

      prefixIcon: Icon(icon),

      filled: true,

      fillColor: Colors.grey.shade100,

      border: OutlineInputBorder(
        borderRadius: BorderRadius.circular(15),
        borderSide: BorderSide.none,
      ),

      enabledBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(15),
        borderSide: BorderSide.none,
      ),

      focusedBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(15),
        borderSide: const BorderSide(color: Color(0xFF4F46E5), width: 2),
      ),

      contentPadding: const EdgeInsets.symmetric(vertical: 18, horizontal: 15),
    );
  }

  // ==========================================================
  // BUILD LOGIN PAGE
  // ==========================================================

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        width: double.infinity,

        height: double.infinity,

        decoration: const BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topLeft,

            end: Alignment.bottomRight,

            colors: [Color(0xFF4F46E5), Color(0xFF7C3AED), Color(0xFF9333EA)],
          ),
        ),

        child: SafeArea(
          child: Center(
            child: SingleChildScrollView(
              padding: const EdgeInsets.all(25),

              child: Container(
                constraints: const BoxConstraints(maxWidth: 430),

                padding: const EdgeInsets.all(30),

                decoration: BoxDecoration(
                  color: Colors.white,

                  borderRadius: BorderRadius.circular(30),

                  boxShadow: [
                    BoxShadow(
                      color: Colors.black.withValues(alpha: 0.2),

                      blurRadius: 30,

                      offset: const Offset(0, 15),
                    ),
                  ],
                ),

                child: Column(
                  children: [
                    // ------------------------------------------------
                    // LOGO
                    // ------------------------------------------------

                    Container(
                      width: 80,

                      height: 80,

                      decoration: BoxDecoration(
                        gradient: const LinearGradient(
                          colors: [Color(0xFF4F46E5), Color(0xFF9333EA)],
                        ),

                        borderRadius: BorderRadius.circular(25),
                      ),

                      child: const Icon(
                        Icons.lock_outline,

                        color: Colors.white,

                        size: 40,
                      ),
                    ),

                    const SizedBox(height: 25),

                    // ------------------------------------------------
                    // TITLE
                    // ------------------------------------------------
                    const Text(
                      "Welcome Back",

                      style: TextStyle(
                        fontSize: 30,

                        fontWeight: FontWeight.bold,

                        color: Color(0xFF1F2937),
                      ),
                    ),

                    const SizedBox(height: 8),

                    Text(
                      "Login to continue to your account",

                      style: TextStyle(
                        fontSize: 15,

                        color: Colors.grey.shade600,
                      ),
                    ),

                    const SizedBox(height: 35),

                    // ------------------------------------------------
                    // EMAIL
                    // ------------------------------------------------
                    TextField(
                      controller: emailController,

                      keyboardType: TextInputType.emailAddress,

                      decoration: inputDecoration(
                        label: "Email Address",

                        icon: Icons.email_outlined,
                      ),
                    ),

                    const SizedBox(height: 18),

                    // ------------------------------------------------
                    // PASSWORD
                    // ------------------------------------------------
                    TextField(
                      controller: passwordController,

                      obscureText: obscurePassword,

                      decoration:
                          inputDecoration(
                            label: "Password",

                            icon: Icons.lock_outline,
                          ).copyWith(
                            suffixIcon: IconButton(
                              icon: Icon(
                                obscurePassword
                                    ? Icons.visibility_off_outlined
                                    : Icons.visibility_outlined,
                              ),

                              onPressed: () {
                                setState(() {
                                  obscurePassword = !obscurePassword;
                                });
                              },
                            ),
                          ),
                    ),

                    const SizedBox(height: 12),

                    // ------------------------------------------------
                    // FORGOT PASSWORD
                    // ------------------------------------------------
                    Align(
                      alignment: Alignment.centerRight,

                      child: TextButton(
                        onPressed: () {
                          setState(() {
                            message = "Forgot password feature coming soon";

                            loginSuccess = false;
                          });
                        },

                        child: const Text(
                          "Forgot Password?",

                          style: TextStyle(
                            color: Color(0xFF4F46E5),

                            fontWeight: FontWeight.w600,
                          ),
                        ),
                      ),
                    ),

                    const SizedBox(height: 10),

                    // ------------------------------------------------
                    // LOGIN BUTTON
                    // ------------------------------------------------
                    SizedBox(
                      width: double.infinity,

                      height: 55,

                      child: ElevatedButton(
                        onPressed: loading ? null : login,

                        style: ElevatedButton.styleFrom(
                          backgroundColor: const Color(0xFF4F46E5),

                          foregroundColor: Colors.white,

                          elevation: 5,

                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(15),
                          ),
                        ),

                        child: loading
                            ? const SizedBox(
                                width: 25,

                                height: 25,

                                child: CircularProgressIndicator(
                                  strokeWidth: 3,

                                  color: Colors.white,
                                ),
                              )
                            : const Text(
                                "LOGIN",

                                style: TextStyle(
                                  fontSize: 16,

                                  fontWeight: FontWeight.bold,

                                  letterSpacing: 1,
                                ),
                              ),
                      ),
                    ),

                    const SizedBox(height: 20),

                    // ------------------------------------------------
                    // MESSAGE
                    // ------------------------------------------------
                    if (message.isNotEmpty)
                      Container(
                        width: double.infinity,

                        padding: const EdgeInsets.all(14),

                        decoration: BoxDecoration(
                          color: loginSuccess
                              ? Colors.green.shade50
                              : Colors.red.shade50,

                          borderRadius: BorderRadius.circular(12),

                          border: Border.all(
                            color: loginSuccess
                                ? Colors.green.shade200
                                : Colors.red.shade200,
                          ),
                        ),

                        child: Text(
                          message,

                          textAlign: TextAlign.center,

                          style: TextStyle(
                            color: loginSuccess
                                ? Colors.green.shade700
                                : Colors.red.shade700,

                            fontWeight: FontWeight.w600,
                          ),
                        ),
                      ),

                    const SizedBox(height: 25),

                    // ------------------------------------------------
                    // REGISTER LINK
                    // ------------------------------------------------
                    Row(
                      mainAxisAlignment: MainAxisAlignment.center,

                      children: [
                        Text(
                          "Don't have an account?",

                          style: TextStyle(color: Colors.grey.shade600),
                        ),

                        TextButton(
                          onPressed: () {
                            Navigator.push(
                              context,

                              MaterialPageRoute(
                                builder: (context) => const RegisterPage(),
                              ),
                            );
                          },

                          child: const Text(
                            "Register",

                            style: TextStyle(
                              color: Color(0xFF4F46E5),

                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }

  // ==========================================================
  // DISPOSE
  // ==========================================================

  @override
  void dispose() {
    emailController.dispose();

    passwordController.dispose();

    super.dispose();
  }
}

// ################################################################
// REGISTER PAGE
// ################################################################

class RegisterPage extends StatefulWidget {
  const RegisterPage({super.key});

  @override
  State<RegisterPage> createState() => _RegisterPageState();
}

class _RegisterPageState extends State<RegisterPage> {
  // ==========================================================
  // CONTROLLERS
  // ==========================================================

  final nameController = TextEditingController();

  final emailController = TextEditingController();

  final mobileController = TextEditingController();

  final passwordController = TextEditingController();

  final confirmPasswordController = TextEditingController();

  // ==========================================================
  // VARIABLES
  // ==========================================================

  bool loading = false;

  bool obscurePassword = true;

  bool obscureConfirmPassword = true;

  String message = "";

  bool registrationSuccess = false;

  // ==========================================================
  // REGISTER FUNCTION
  // ==========================================================

  Future<void> register() async {
    // --------------------------------------------------------
    // Validate fields
    // --------------------------------------------------------

    if (nameController.text.trim().isEmpty ||
        emailController.text.trim().isEmpty ||
        mobileController.text.trim().isEmpty ||
        passwordController.text.isEmpty ||
        confirmPasswordController.text.isEmpty) {
      setState(() {
        message = "Please fill all fields";

        registrationSuccess = false;
      });

      return;
    }

    // --------------------------------------------------------
    // Check password
    // --------------------------------------------------------

    if (passwordController.text != confirmPasswordController.text) {
      setState(() {
        message = "Passwords do not match";

        registrationSuccess = false;
      });

      return;
    }

    // --------------------------------------------------------
    // Check password length
    // --------------------------------------------------------

    if (passwordController.text.length < 6) {
      setState(() {
        message = "Password must be at least 6 characters";

        registrationSuccess = false;
      });

      return;
    }

    setState(() {
      loading = true;

      message = "";

      registrationSuccess = false;
    });

    try {
      print("======================================");

      print("REGISTRATION STARTED");

      print("API URL: $baseUrl/register");

      print("======================================");

      // ======================================================
      // SEND REGISTRATION REQUEST
      // ======================================================

      final response = await http
          .post(
            Uri.parse("$baseUrl/register"),

            headers: {
              "Content-Type": "application/json",

              "Accept": "application/json",
            },

            body: jsonEncode({
              "name": nameController.text.trim(),

              "email": emailController.text.trim(),

              "password": passwordController.text,

              "mobile": mobileController.text.trim(),
            }),
          )
          .timeout(const Duration(seconds: 15));

      // ======================================================
      // PRINT RESPONSE
      // ======================================================

      print(
        "REGISTER STATUS: "
        "${response.statusCode}",
      );

      print(
        "REGISTER RESPONSE: "
        "${response.body}",
      );

      // ======================================================
      // DECODE RESPONSE
      // ======================================================

      final data = jsonDecode(response.body);

      // ======================================================
      // REGISTRATION SUCCESS
      // ======================================================

      if (response.statusCode == 200) {
        setState(() {
          message = "Registration successful!";

          registrationSuccess = true;
        });

        // ----------------------------------------------------
        // Wait and return to login page
        // ----------------------------------------------------

        await Future.delayed(const Duration(seconds: 1));

        if (mounted) {
          Navigator.pop(context);
        }
      }
      // ======================================================
      // REGISTRATION ERROR
      // ======================================================
      else {
        setState(() {
          message = data["detail"] ?? "Registration failed";

          registrationSuccess = false;
        });
      }
    }
    // ========================================================
    // CONNECTION ERROR
    // ========================================================
    catch (e) {
      print("REGISTRATION ERROR: $e");

      setState(() {
        message = "Connection error:\n$e";

        registrationSuccess = false;
      });
    }
    // ========================================================
    // STOP LOADING
    // ========================================================
    finally {
      if (mounted) {
        setState(() {
          loading = false;
        });
      }
    }
  }

  // ==========================================================
  // INPUT DECORATION
  // ==========================================================

  InputDecoration inputDecoration({
    required String label,

    required IconData icon,
  }) {
    return InputDecoration(
      labelText: label,

      prefixIcon: Icon(icon),

      filled: true,

      fillColor: Colors.grey.shade100,

      border: OutlineInputBorder(
        borderRadius: BorderRadius.circular(15),

        borderSide: BorderSide.none,
      ),

      enabledBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(15),

        borderSide: BorderSide.none,
      ),

      focusedBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(15),

        borderSide: const BorderSide(color: Color(0xFF4F46E5), width: 2),
      ),

      contentPadding: const EdgeInsets.symmetric(vertical: 18, horizontal: 15),
    );
  }

  // ==========================================================
  // BUILD REGISTER PAGE
  // ==========================================================

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        width: double.infinity,

        height: double.infinity,

        decoration: const BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topLeft,

            end: Alignment.bottomRight,

            colors: [Color(0xFF4F46E5), Color(0xFF7C3AED), Color(0xFF9333EA)],
          ),
        ),

        child: SafeArea(
          child: Center(
            child: SingleChildScrollView(
              padding: const EdgeInsets.all(25),

              child: Container(
                constraints: const BoxConstraints(maxWidth: 430),

                padding: const EdgeInsets.all(30),

                decoration: BoxDecoration(
                  color: Colors.white,

                  borderRadius: BorderRadius.circular(30),

                  boxShadow: [
                    BoxShadow(
                      color: Colors.black.withValues(alpha: 0.2),

                      blurRadius: 30,

                      offset: const Offset(0, 15),
                    ),
                  ],
                ),

                child: Column(
                  children: [
                    // ==================================================
                    // REGISTER ICON
                    // ==================================================

                    Container(
                      width: 80,

                      height: 80,

                      decoration: BoxDecoration(
                        gradient: const LinearGradient(
                          colors: [Color(0xFF4F46E5), Color(0xFF9333EA)],
                        ),

                        borderRadius: BorderRadius.circular(25),
                      ),

                      child: const Icon(
                        Icons.person_add_alt_1,

                        color: Colors.white,

                        size: 40,
                      ),
                    ),

                    const SizedBox(height: 20),

                    // ==================================================
                    // TITLE
                    // ==================================================
                    const Text(
                      "Create Account",

                      style: TextStyle(
                        fontSize: 30,

                        fontWeight: FontWeight.bold,

                        color: Color(0xFF1F2937),
                      ),
                    ),

                    const SizedBox(height: 8),

                    Text(
                      "Register to create your account",

                      style: TextStyle(
                        fontSize: 15,

                        color: Colors.grey.shade600,
                      ),
                    ),

                    const SizedBox(height: 30),

                    // ==================================================
                    // NAME
                    // ==================================================
                    TextField(
                      controller: nameController,

                      keyboardType: TextInputType.name,

                      decoration: inputDecoration(
                        label: "Full Name",

                        icon: Icons.person_outline,
                      ),
                    ),

                    const SizedBox(height: 16),

                    // ==================================================
                    // EMAIL
                    // ==================================================
                    TextField(
                      controller: emailController,

                      keyboardType: TextInputType.emailAddress,

                      decoration: inputDecoration(
                        label: "Email Address",

                        icon: Icons.email_outlined,
                      ),
                    ),

                    const SizedBox(height: 16),

                    // ==================================================
                    // MOBILE
                    // ==================================================
                    TextField(
                      controller: mobileController,

                      keyboardType: TextInputType.phone,

                      decoration: inputDecoration(
                        label: "Mobile Number",

                        icon: Icons.phone_outlined,
                      ),
                    ),

                    const SizedBox(height: 16),

                    // ==================================================
                    // PASSWORD
                    // ==================================================
                    TextField(
                      controller: passwordController,

                      obscureText: obscurePassword,

                      decoration:
                          inputDecoration(
                            label: "Password",

                            icon: Icons.lock_outline,
                          ).copyWith(
                            suffixIcon: IconButton(
                              icon: Icon(
                                obscurePassword
                                    ? Icons.visibility_off_outlined
                                    : Icons.visibility_outlined,
                              ),

                              onPressed: () {
                                setState(() {
                                  obscurePassword = !obscurePassword;
                                });
                              },
                            ),
                          ),
                    ),

                    const SizedBox(height: 16),

                    // ==================================================
                    // CONFIRM PASSWORD
                    // ==================================================
                    TextField(
                      controller: confirmPasswordController,

                      obscureText: obscureConfirmPassword,

                      decoration:
                          inputDecoration(
                            label: "Confirm Password",

                            icon: Icons.lock_reset_outlined,
                          ).copyWith(
                            suffixIcon: IconButton(
                              icon: Icon(
                                obscureConfirmPassword
                                    ? Icons.visibility_off_outlined
                                    : Icons.visibility_outlined,
                              ),

                              onPressed: () {
                                setState(() {
                                  obscureConfirmPassword =
                                      !obscureConfirmPassword;
                                });
                              },
                            ),
                          ),
                    ),

                    const SizedBox(height: 25),

                    // ==================================================
                    // REGISTER BUTTON
                    // ==================================================
                    SizedBox(
                      width: double.infinity,

                      height: 55,

                      child: ElevatedButton(
                        onPressed: loading ? null : register,

                        style: ElevatedButton.styleFrom(
                          backgroundColor: const Color(0xFF4F46E5),

                          foregroundColor: Colors.white,

                          elevation: 5,

                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(15),
                          ),
                        ),

                        child: loading
                            ? const SizedBox(
                                width: 25,

                                height: 25,

                                child: CircularProgressIndicator(
                                  strokeWidth: 3,

                                  color: Colors.white,
                                ),
                              )
                            : const Text(
                                "CREATE ACCOUNT",

                                style: TextStyle(
                                  fontSize: 15,

                                  fontWeight: FontWeight.bold,

                                  letterSpacing: 1,
                                ),
                              ),
                      ),
                    ),

                    const SizedBox(height: 20),

                    // ==================================================
                    // MESSAGE
                    // ==================================================
                    if (message.isNotEmpty)
                      Container(
                        width: double.infinity,

                        padding: const EdgeInsets.all(14),

                        decoration: BoxDecoration(
                          color: registrationSuccess
                              ? Colors.green.shade50
                              : Colors.red.shade50,

                          borderRadius: BorderRadius.circular(12),

                          border: Border.all(
                            color: registrationSuccess
                                ? Colors.green.shade200
                                : Colors.red.shade200,
                          ),
                        ),

                        child: Text(
                          message,

                          textAlign: TextAlign.center,

                          style: TextStyle(
                            color: registrationSuccess
                                ? Colors.green.shade700
                                : Colors.red.shade700,

                            fontWeight: FontWeight.w600,
                          ),
                        ),
                      ),

                    const SizedBox(height: 15),

                    // ==================================================
                    // BACK TO LOGIN
                    // ==================================================
                    Row(
                      mainAxisAlignment: MainAxisAlignment.center,

                      children: [
                        Text(
                          "Already have an account?",

                          style: TextStyle(color: Colors.grey.shade600),
                        ),

                        TextButton(
                          onPressed: () {
                            Navigator.pop(context);
                          },

                          child: const Text(
                            "Login",

                            style: TextStyle(
                              color: Color(0xFF4F46E5),

                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }

  // ==========================================================
  // DISPOSE
  // ==========================================================

  @override
  void dispose() {
    nameController.dispose();

    emailController.dispose();

    mobileController.dispose();

    passwordController.dispose();

    confirmPasswordController.dispose();

    super.dispose();
  }
}
