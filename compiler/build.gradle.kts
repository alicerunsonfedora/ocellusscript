import org.jetbrains.kotlin.gradle.tasks.KotlinCompile

/*
 * This file was generated by the Gradle 'init' task.
 *
 * This generated file contains a sample Kotlin application project to get you started.
 */

plugins {
    // Apply the Kotlin Multiplatform plugin to add support for Kotlin.
    kotlin("multiplatform") version "1.3.70"
    id("org.jetbrains.dokka") version "0.10.0"
}

repositories {
    jcenter()
    mavenCentral()
}

kotlin {
    jvm()
    js()
    wasm32()
}

kotlin.sourceSets["commonMain"].dependencies {
    implementation(kotlin("stdlib-jdk8"))
    implementation(kotlin("stdlib-common"))
}

kotlin.sourceSets["jvmMain"].dependencies {
    implementation(kotlin("stdlib-jdk8"))
    implementation(kotlin("stdlib-common"))
    implementation("com.xenomachina:kotlin-argparser:2.0.7")
}

kotlin.sourceSets["jvmMain"].dependencies {
    implementation(kotlin("stdlib-jdk8"))
    implementation(kotlin("stdlib-common"))
    implementation(kotlin("test-common"))
    implementation(kotlin("test-annotations-common"))
}

val run by tasks.creating(JavaExec::class) {
  group = "application"
  main = "net.marquiskurt.ocls.compiler.AppKt"
  kotlin {
    val main = targets["jvm"].compilations["main"]
    dependsOn(main.compileAllTaskName)
    classpath(
            { main.output.allOutputs.files },
            { configurations["jvmRuntimeClasspath"] }
    )
  }
  ///disable app icon on macOS
  systemProperty("java.awt.headless", "true")
}