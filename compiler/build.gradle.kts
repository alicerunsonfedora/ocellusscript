import org.jetbrains.kotlin.gradle.tasks.KotlinCompile
import org.gradle.jvm.tasks.Jar

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
    wasm32()

    sourceSets {
        val commonMain by getting {
            dependencies {
                implementation(kotlin("stdlib-jdk8"))
                implementation(kotlin("stdlib-common"))
            }
        }
        val jvmMain by getting {
            dependencies {
                implementation(kotlin("stdlib-jdk8"))
                implementation(kotlin("stdlib-common"))
                implementation("com.xenomachina:kotlin-argparser:2.0.7")
            }
        }

        val wasm32Main by getting {
            dependencies {
                implementation(kotlin("stdlib-js"))
                implementation(kotlin("stdlib-common"))
            }
        }

        val jvmTest by getting {
            dependencies {
                implementation(kotlin("stdlib-jdk8"))
                implementation(kotlin("stdlib-common"))
                implementation(kotlin("test-common"))
                implementation(kotlin("test-annotations-common"))
            }
        }
    }
}

tasks.dokka {
    outputFormat = "html"
    multiplatform {
        register("jvmMain") { // Different name, so source roots must be passed explicitly
            targets = listOf("JVM")
            platform = "jvm"
            sourceRoot {
                path = kotlin.sourceSets.getByName("jvmMain").kotlin.srcDirs.first().toString()
            }
        }
        register("commonMain") {
            targets = listOf("Common")
            platform = "common"
            sourceRoot {
                path = kotlin.sourceSets.getByName("commonMain").kotlin.srcDirs.first().toString()
            }
        }
    }
}

tasks.create<Jar>("nocJar") {
    manifest {
        attributes(mapOf("Main-Class" to "net.marquiskurt.ocls.compiler.NOCAppJVMKt"))
    }
    kotlin {
        val sourceMain = targets["jvm"].compilations["main"]
        dependsOn(sourceMain.compileAllTaskName)
        from(sourceMain.output)
//        sourceMain.compileDependencyFiles
//                .filter { it.name.endsWith("jar") }
//                .forEach { jar -> from(zipTree(jar)) }
    }

}

val run by tasks.creating(JavaExec::class) {
    group = "application"
    main = "net.marquiskurt.ocls.compiler.NOCAppJVMKt"
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